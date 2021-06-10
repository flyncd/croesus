croesus_randomiser

Sample Oracle which demonstrates a full end-to-end example of a crosesus application

Python Flask app which exposes an endpoint GET /random which produces the following result:


{
    "uuid": "200505-AE62-44ABB-83AFD"
    ,"consumer": "test_user"
    ,"type": "request"
    , "value": 0.83028
}

For use cases where an outcome or reporting endpoint is required. This would require some form of authentication to ensure that
the requestor attached to the original UUID had the permissions to assign an outcome.

Elements required:
    * Service itself (randomiser function)
    * All requests logged to some output / log sink, which can then be captured / handled by the croesus_processor


