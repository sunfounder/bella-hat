#!/bin/bash

set -e  # Exit immediately if a command exits with non-zero status

# Get the directory of the current script
PRJ_PATH=$(dirname $(dirname $(realpath $0)))
. "$PRJ_PATH/certificate/message.sh"

info "BELLA ROBOT STARTUP SEQUENCE INITIATED"

# Stop the existing process
info "Stopping any existing Bella services..."
$PRJ_PATH/certificate/stop.sh
success "Previous services stopped"

VENV_FOLDER="$PRJ_PATH/.venv"

configure_audio() {
    local speaker_volume=$1
    info "Configuring audio devices with speaker volume: $speaker_volume..."
    sudo "$PRJ_PATH/certificate/configure_audio.sh" "$speaker_volume"
}

# Start a server
start_server() {
    local SERVER_COMMAND=$1
    local SERVER_NAME=$2

    info "Starting server $SERVER_NAME with command: $SERVER_COMMAND"
    
    MAX_ATTEMPTS=5
    ATTEMPT=1
    SERVER_STARTED=false

    while [ $ATTEMPT -le $MAX_ATTEMPTS ] && [ "$SERVER_STARTED" = false ]; do
        info "Attempt $ATTEMPT of $MAX_ATTEMPTS to start server $SERVER_NAME..."
        
        # Start the Glow server
        screen -dm -S $SERVER_NAME bash -c "source $VENV_FOLDER/bin/activate; cd $PRJ_PATH/certificate; $SERVER_COMMAND &> logs/$SERVER_NAME.log"
        
        # Wait a moment for the process to start
        sleep 2
        
        # Check if the screen session is still running
        if screen -list | grep -q "$SERVER_NAME"; then
            # Check if there's a process running inside the screen
            pid=$(screen -S $SERVER_NAME -Q echo '$PID')
            if [ -n "$pid" ] && ps -p $pid > /dev/null; then
                SERVER_STARTED=true
                success "$SERVER_NAME started in screen session '$SERVER_NAME'"
            else
                warn "$SERVER_NAME process died immediately in attempt $ATTEMPT"
                screen -S $SERVER_NAME -X quit 2>/dev/null
            fi
        else
            warn "$SERVER_NAME screen session not found in attempt $ATTEMPT"
        fi
        
        if [ "$SERVER_STARTED" = false ]; then
            ATTEMPT=$((ATTEMPT+1))
            [ $ATTEMPT -le $MAX_ATTEMPTS ] && sleep 3
        fi
    done
    
    if [ "$SERVER_STARTED" = true ]; then
        return 0
    else
        return 1
    fi
}

run_servers() {
    MAIN_SERVER="uvicorn app:app --host 0.0.0.0 --port 8000"

    MAIN_SERVER_STARTED=$(start_server "$MAIN_SERVER" "app")
    if [ "$MAIN_SERVER_STARTED" = 1 ]; then
        error "Failed to start main application"
    fi
}

usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Start Bella Robot software"
    echo ""
    echo "Options:"
    echo "  -h, --help      Display this help message"
    echo "  -v, --version   Display version information"
}

### main

main () {
    if [ $# -gt 0 ]
    then
        case $1 in
            --help|-h)
                usage
                exit 0
                ;;
            --version|-v)
                msg "${Version:-1.0.0}"
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    else
        info "Starting Bella Robot software..."

        configure_audio "100%"

        run_servers
    fi
}

main "$@"