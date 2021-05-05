# Schema Definition

## Purpose

Create a standards-based structure for the registration and assessment of automated services

## Investigate

Extend the schema.org SolveMathAction and MathSolver schemas

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

The Cardano meta data calls for a leaner standard compared with what schema.org has proposed.

We will instead target this leaner standard, which is domain-specific to our purpose.

## Workflow

### Actors

API Developer

Creates an application which solves a problem, or addresses some need.

Node Operator

Pays the API some licence fee to host their application and charges End Users for requests

End User

Uses the application to solve their problem

### Process

An API developer creates an application which returns a random number. The API exposes the following simple endpoints:

GET /random

which returns values like:

```
{ "uuid": "200505-AE62-44ABB-83AFD", "value": 0.83028 }
```

The application also comes bundled with an aggregator script which aggregates logged records into metrics relevant to the application.

During execution the application emits a log line of the returned value to standard out, which can be captured by an application log.

Periodically, depending on the applications reporting period, a monitoring sweep or log rotation is executed which:

- Collates all requests into a response file
- Aggregates requests into a set of metrics as defined by the API developer using the aggregator script
- Makes the collated log file available via a monitoring endpoint, or URL
- Publishes a Cardano blockchain transaction with the aggregated metric values and a link to the collated log file

The Node operator maintains this application with a configuration file which specifies:

* How often to run the log rotation
* Where to publish the collated response file

The Node operator is incentivised to do this because it provides some value-added features to their node, the Node Operator can seel access to the API to end users and offer discounts to End Users who stake with them.

End Users enters into a contract with the Node Operator to access API, and can assess the performance of the service by querying the Croesus metadata stored on the Cardano blockchain

### Metadata - Registration

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
            ,"version": "1.00"
            ,"endpoint": "//mydomain.com/randomiser/v1/random"
            ,"specification": "//randomiser.com"
            ,"reporting":
                {
                    "endpoint": "//mydomain.com/randomiser/v1/monitoring"
                    ,"metrics": ["requests","distribution"]
                }
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
            ,"type": "registration"
            ,"reference": "r43fh9fvh4v4v45g35rh5g3hg53g35"
        }
    "1":
        {
            "name": "Randomiser"
            ,"purpose": "Produce Random Numbers Between 0 and 1"
            ,"version": "2.00"
            ,"endpoint": "//mydomain.com/randomiser/v2/random"
            ,"specification": "//randomiser.com"
            ,"reporting":
                {
                    "endpoint": "//mydomain.com/randomiser/v2/monitoring"
                    ,"metrics": ["requests","distribution"]
                }
        }
}
```

This transaction is made out to the API developer's wallet, and accompanied by an amount which has been agreed to between the developer and the node operator.

This will result in a transaction id being created

"aaaad5222e1be60bd41988679ddb2dbc77e757b39adfed63811dabf9b3065d2e"

### Structure - Confirmation

There is now a requirement for the API developer to verify that the registration is valid.

They can confirm this by creating another transaction sent back to the Node Operator's wallet.

This pair of transactions - a registration and follow up confirmation - establishes confidence that the service is trustworthy and aligned with developer expectations.

Only registrations which have a paired confirmation will be aggregateed when assessing the application's performance.

Confirmation meta data takes the form:

```
{
    "0": {
            "system": "croesus"
            ,"type": "confirmation"
            ,"reference": "aaaad5222e1be60bd41988679ddb2dbc77e757b39adfed63811dabf9b3065d2e"
        }
}
```

where the reference is the transaction id from the registration.

This will result in a transaction id being created, which either wallet can reference in a termination transaction, or the node operator can reference in a reporting transaction

"f098d5222e1be60bd41988679ddb2dbc77e757b39adfed63811dabf9b3065d2e"

### Structure - Termination

A mechanism should exist which allows either the API developer, or the Node Operator to indicate the service is terminated

This payload, is of course only binding if the API developer's wallet or Node Operator's wallet is used process the request

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
                                    ,"value": 100.0
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
            }
}
```

### Structure - Investigation

Verification reports should include a paired investigation which can assess whether verifications of reports are valid or invalid. These investigations 

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
