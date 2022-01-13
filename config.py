class Config :
    JWT_SECRET_KEY = 'yh@1234'
    S3_BUCKET = "block-yh-test"
    S3_KEY = "AKIAZG3RSB5PSZ7BTOPV"
    S3_SECRET = "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"
    S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
