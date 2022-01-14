class Config :
    JWT_SECRET_KEY = 'yh@1234'

    ACCESS_KEY = "AKIAXNC6VFCRCVPEDHM4"
    SECRET_ACCESS = "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"

    S3_BUCKET = "jkong-image-test"
    S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
