FROM namshi/smtp:latest

# entrypoint_file: /bin/entrypoint.sh
RUN sed -i '1 a export GMAIL_USER=$(cat $GMAIL_USER_FILE)' /bin/entrypoint.sh \
    && sed -i '2 a export GMAIL_PASSWORD=$(cat $GMAIL_PASSWORD_FILE)' /bin/entrypoint.sh
