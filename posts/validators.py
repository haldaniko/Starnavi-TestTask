from profanity_check import predict


def validate_profanity(content):
    return predict([content])[0] == 1
