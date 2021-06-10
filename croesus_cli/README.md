
croesus_processor

Sample application which handles logged records for a given service 

cron job / collection of scripts which:

    * Periodically aggregates logs from an application 
        - publish logs [internal, to storage bucket, github, custom -- configurable, using IPFS for sample application ]
        - applies a metric [GitHub repository would feature some basic ones, allowing pull requests for others]
            * Request Count [how many records are in the logs being processed]
            * Bucket_Distribution [ for a given value found in the logs eg "value", break it up into buckets of range X
            * Categorical_Distribution [ for a given value found in the logs, count distinct records for each value]
            * Gini [ for a given value and associated outcome calculate distribution of Goods to Bads ]
        - creates croesus cardano meta data transactions
            - Registration
            - Offering
            - Confirmation
            - Termination
            - Reporting
            - Verification
            - Investigation

