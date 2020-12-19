# Automated Number Plate Recognition with Amazon SageMaker

This project uses the Amazon SageMaker customer inference container functionality to host a 
pretrained model for automated license plate recognition (ANPR). The inference code with a 
model server to serve the predictions is packaged in a SageMaker-compatible Docker container.
The pretrained model and some code for inference and preprocessing relies on [this](https://github.com/quangnhat185/Plate_detect_and_recognize) repo by the
GitHub user quagnhat285.

## Usage

### Creating the SageMaker Endpoint

To deploy the model to a SageMaker endpoint, you need to build the Docker container and upload it
to Amazon ECR. Also, you need to put the model artifacts into an S3 bucket, zipped as *.tar.gz*. 
Once everything is uploaded, you can refernce both the inference image and the model artifacts 
when you create a model with the `CreateModel` API call or in the AWS Console. Follow the guide 
in the [AWS Docs](https://docs.aws.amazon.com/sagemaker/latest/dg/deploy-model.html).

### Running inference

The model endpoint accepts jpg images through a POST request with the mime-type `application/x-image`. Please refer
to the test subdirectory in this repo to see an example of an API call with the boto3 SDK. The endpoint returns an object
of `application/json` with the following format (`img_lp` is the cropped licenseplate image and `coords_lp` are the coordinates of the licenseplate
in the original image):
```json
{
    "img_lp": [[[[...]]]],
    "coords_lp": [[[...]]], 
}
```

### Testing

You can use the provided test script together with the test images to test the SageMaker endpoint as follows:

```bash
python3 test_sm.py img/golf.jpg --output inference.jpg
```