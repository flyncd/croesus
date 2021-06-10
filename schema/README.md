# Schema Definition

## Purpose

Create a standards-based structure for the registration and assessment of automated services

## Investigate

What are the elements necessary to track performance of oracles that serve a decentralised ecosystem?

## Results

Cardano transaction meta data carries a 16k limit. Structural limitations are described here:

https://github.com/input-output-hk/cardano-node/blob/master/doc/reference/tx-metadata.md#:~:text=of%20the%20metadata.-,Metadata%20structure,what%20the%20metadata%20value%20is

The example structure which we will pursue with this project is:

```
{
"0": {"key": "value"}
"1": {"key": "value"}
}
```

The Cardano meta data calls for a leaner standard compared with what schema.org has proposed for example.

We have instead target a leaner standard, which is domain-specific to our purpose.

## Workflow


[image]

### Actors

API Developer

Creates an service which solves a problem, or addresses some need.

Node Operator

Hosts a service on behalf of the API Developer
Contract to do so made between API Developer and Node Operator subject to their own agreement.

End User

Uses the service to solve their problem
Contract to do so made between Node Operator and End User

### Process

An API developer creates a service which returns a random number. The API exposes the following simple endpoints:

GET /random

which returns values like:

```
{ "uuid": "200505-AE62-44ABB-83AFD", "value": 0.83028 }
```

The service also comes bundled with an croesus aggregator script which aggregates logged records into metrics relevant to the application.

During execution the application emits a log line of the returned value to standard out, which can be captured by an application log.

Periodically, depending on the applications reporting period, a monitoring sweep or log rotation is executed which:

- Collates all requests into a response file
- Aggregates requests into a set of metrics as defined by the API developer using the aggregator script
- Makes the collated log file available via a monitoring endpoint, or URL
- Publishes a Cardano blockchain transaction with the aggregated metric values and a link to the collated log file

The Node operator maintains this application with a configuration file which specifies:

* How often to run the log rotation
* Where to publish the collated response file
* What is the keyfile used to sign metadata transactions

The Node operator is incentivised to do this because it provides some value-added features to their node, the Node Operator can sell access to the API to end users and offer discounts to End Users who stake with them.

End Users enters into a contract with the Node Operator to access API, and can assess the performance of the service by querying the Croesus metadata stored on the Cardano blockchain

### Metadata - Application Registration

```
{
    "0":
        {
            "system": "croesus"
            ,"type": "registration"
        }
    "1":
        {
            "name": "Randomiser"
            ,"purpose": "Produce Random Numbers Between 0 and 1"
            ,"codebase": "github.//"
            ,"metrics": ["distribution"]
            ,"specification": "A reference to the specification of this service. eg) IPFS file which species input data, output schema and outcome / reference and sample data to validate model. Left vague on purpose to support many types of services"
        }
}
```

This transaction is made out to the API developer's wallet, registers an application which can be sold on a marketplace to an API hoster.

This will result in a transaction id being created

"f4h29f942b9vb9v9vb89b89b89vb24"

### Metadata - Offering

```
{
    "0":
        {
            "system": "croesus"
            ,"type": "offering"
            ,"registration": "f4h29f942b9vb9v9vb89b89b89vb24" // a reference to the service registration metadata
        }
    "1":
        {
            ,"version": "1.00"
            ,"endpoint": "//mydomain.com/randomiser/v1/random"
        }
}
```

If replacing an older registration, an optional "reference" field can be added in the meta data request. This is a reference to the confirmation of the associated former registration.

This is used so that reporting on metrics across versions can occur.

eg)

```
{
    "0":
        {
            "system": "croesus"
            ,"type": "offering"
            ,"registration": "f4h29f942b9vb9v9vb89b89b89vb24" // a reference to the service registration metadata
        }
    "1":
        {
            ,"version": "2.00"
            ,"endpoint": "//mydomain.com/randomiser/v1/random"
        }
}
```

This transaction is made out to the API developer's wallet, and accompanied by an amount which has been agreed to between the developer and the node operator.

This will result in a transaction id being created

"aaaad5222e1be60bd41988679ddb2dbc77e757b39adfed63811dabf9b3065d2e"

### Structure - Confirmation

There is an optional step for an API developer to verify that the registration is valid.

This operates something like a certification which can be filtered out when aggregating results.

Perhaps only those performance metrics which have been certified are worthwhile

They can confirm this by creating another transaction sent back to the Node Operator's wallet.

This pair of transactions - a registration and follow up confirmation - establishes confidence that the service is trustworthy and aligned with developer expectations.

Confirmation meta data takes the form:

```
{
    "0": {
            "system": "croesus"
            ,"type": "confirmation"
            ,"offering": "aaaad5222e1be60bd41988679ddb2dbc77e757b39adfed63811dabf9b3065d2e"
        }
}
```

where the reference is the transaction id from the registration.

This will result in a transaction id being created, which either wallet can reference in a termination transaction, or the node operator can reference in a reporting transaction

"f098d5222e1be60bd41988679ddb2dbc77e757b39adfed63811dabf9b3065d2e"

### Structure - Termination

A mechanism should exist which allows either the API developer, or the Node Operator to indicate the service is terminated

This payload, is of course only binding if the API developer's wallet or Node Operator's wallet is used process the request. Any layer which aggregates this data should understand this distinction, otherwise anyone could specify
termination requests.

```
{
    "0":   {
                "system": "croesus"
                ,"type": "termination"
                ,"reference": "f098d5222e1be60bd41988679ddb2dbc77e757b39adfed63811dabf9b3065d2e"
            } 
}
```

This establishes a protocol for two use cases:

1) Gracefully informating the ecosystem that an API endpoint is no longer available
2) Allowing developers who no longer have trust in a Node Operator to terminate the reporting of performance metrics

### Structure - Reporting

The reporting of metrics must be made by the Node Operator who created the registration, with the form of the report containing:

```
{
    "0":    {
                "system": "croesus"
                ,"type": "report"
                ,"reference": "f098d5222e1be60bd41988679ddb2dbc77e757b39adfed63811dabf9b3065d2e"
            }
    ,"1":   {
                "metrics":  [
                                {
                                    "name": "distribution"
                                    ,"value": 93.4
                                }
                                ,{
                                    "name": "requests"
                                    ,"value": 31949520
                                }
                            ]
                ,"validation":  "//mydomain.com/randomiser/v2/monitoring/4fg9f49gb2949b7g497g49g4294g2bg97vb9v49"
            }
}
```

### Structure - Verification

The protocol must include a mechanism for End Users and the broader community to flag issues with reports. Including these as on-chain events allows for flagging misleading performance metrics as invalid.

Verification reports must be sent to an arbitrator with a verified identity (via DID or other mechnism for review)

```
{
    "0":    {
                "system": "croesus"
                ,"type": "verification"
                ,"reference": "f48fh8440f88cb402804242"
                ,"complaint": "I ran a scoring request lasy may with UUID of fdsfds when i check the logs it is;t ther"
            }
}
```

### Structure - Investigation

Verification reports should include a paired investigation which can assess whether verifications of reports are valid or invalid. The nature of verifications and investigations is included in this protocol for completeness, although the form these determinations take is left up to eahc individual service to determine.


```
{
    "0":    {
                "system": "croesus"
                ,"type": "investigation"
                ,"verification_reference": "f48fh8440f88cb402804242"
            }
    ,"1":   {
                "assessment": "upheld"
                "rationale":    [
                                    "The referenced croesus report"
                                    ,"has been investigated"
                                    ,"and judged to be "
                                    ,"incorrect"
                                ]
            }
}
```
