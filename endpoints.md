# Endpoints

This document details the list of endpoints exposed by the REST API and their current 
state in this library.

It was pulled from https://docs.atlassian.com/atlassian-confluence/REST/6.6.0/ so 
is current as of v6.6.0.

State key:
- empty => Not written
- 1 => written but not tested
- 2 => written and tested

Note that there are also TODOs scattered through the code where particular parts of
objects have not yet been expanded.

## audit

| HTTP Type | Endpoint                                                | State |
|-----------|--------------------------------------------------------:|-------|
|GET        |/rest/audit                                              | 1     |
|POST       |/rest/audit                                              |       |
|GET        |/rest/audit/export                                       |       |
|GET        |/rest/audit/retention                                    |       |
|PUT        |/rest/audit/retention                                    |       |
|GET        |/rest/audit/since                                        |       |

## content

| HTTP Type | Endpoint                                                | State |
|-----------|--------------------------------------------------------:|-------|
|POST       |/rest/content                                            |       |
|GET        |/rest/content                                            | 1     |
|PUT        |/rest/content/{contentId}                                | 1     |
|GET        |/rest/content/{id}                                       | 1     |
|DELETE     |/rest/content/{id}                                       |       |
|GET        |/rest/content/{id}/history                               | 1     |
|GET        |/rest/content/{id}/history/{version}/macro/hash/{hash}   |       |
|GET        |/rest/content/{id}/history/{version}/macro/id/{macroId}  |       |
|GET        |/rest/content/search                                     | 1     |

### content/{id}/child

| HTTP Type | Endpoint                                                | State |
|-----------|--------------------------------------------------------:|-------|
|GET        |/rest/content/{id}/child                                 |       |
|GET        |/rest/content/{id}/child/{type}                          | 1     |
|GET        |/rest/content/{id}/child/comment                         | 1     |

### content/{id}/child/attachment

| HTTP Type | Endpoint                                                | State |
|-----------|--------------------------------------------------------:|-------|
|GET        |/rest/content/{id}/child/attachment                      | 1     |
|POST       |/rest/content/{id}/child/attachment                      | 1     |
|PUT        |/rest/content/{id}/child/attachment/{attachmentId}       |       |
|POST       |/rest/content/{id}/child/attachment/{attachmentId}/data  |       |

### content/{id}/descendant

| HTTP Type | Endpoint                                                | State |
|-----------|--------------------------------------------------------:|-------|
|GET        |/rest/content/{id}/descendant                            |       |
|GET        |/rest/content/{id}/descendant/{type}                     |       |

### content/{id}/label

| HTTP Type | Endpoint                                                | State |
|-----------|--------------------------------------------------------:|-------|
|GET        |/rest/content/{id}/label                                 | 1     |
|POST       |/rest/content/{id}/label                                 |       |
|DELETE     |/rest/content/{id}/label                                 |       |
|DELETE     |/rest/content/{id}/label/{label}                         |       |

### content/{id}/property

| HTTP Type | Endpoint                                                | State |
|-----------|--------------------------------------------------------:|-------|
|GET        |/rest/content/{id}/property                              |       |
|POST       |/rest/content/{id}/property                              |       |
|GET        |/rest/content/{id}/property/{key}                        |       |
|PUT        |/rest/content/{id}/property/{key}                        |       |
|DELETE     |/rest/content/{id}/property/{key}                        |       |
|POST       |/rest/content/{id}/property/{key}                        |       |

### content/{id}/restriction

| HTTP Type | Endpoint                                                | State |
|-----------|--------------------------------------------------------:|-------|
|GET        |/rest/content/{id}/restriction/byOperation               |       |
|GET        |/rest/content/{id}/restriction/byOperation/{operationKey}|       |
|POST       |/rest/content/blueprint/instance/{draftId}               |       |
|PUT        |/rest/content/blueprint/instance/{draftId}               |       |

### contentbody/convert/{to}

| HTTP Type | Endpoint                                                | State |
|-----------|--------------------------------------------------------:|-------|
|POST       |/rest/contentbody/convert/{to}                           |       |

## group

| HTTP Type | Endpoint                                                | State |
|-----------|--------------------------------------------------------:|-------|
|GET        |groups                                                   | 1     |
|GET        |group                                                    | 1     |
|GET        |members                                                  | 1     |

## longtask

| HTTP Type | Endpoint                                                | State |
|-----------|--------------------------------------------------------:|-------|
|GET        |/rest/longtask                                           | 1     |
|GET        |/rest/longtask/{id}                                      | 1     |

## search

| HTTP Type | Endpoint                                                | State |
|-----------|--------------------------------------------------------:|-------|
|GET        |/rest/search                                             |       |

## space

| HTTP Type | Endpoint                                                | State |
|-----------|--------------------------------------------------------:|-------|
|GET        |/rest/space                                              | 1     |
|POST       |/rest/space                                              |       |
|POST       |/rest/space/_private                                     |       |
|PUT        |/rest/space/{spaceKey}                                   |       |
|DELETE     |/rest/space/{spaceKey}                                   |       |
|GET        |/rest/space/{spaceKey}                                   | 1     |
|GET        |/rest/space/{spaceKey}/content                           | 1     |
|GET        |/rest/space/{spaceKey}/content/{type}                    | 1     |

### space/{spaceKey}/property

| HTTP Type | Endpoint                                                | State |
|-----------|--------------------------------------------------------:|-------|
|GET        |/rest/space/{spaceKey}/property                          |       |
|POST       |/rest/space/{spaceKey}/property                          |       |
|GET        |/rest/space/{spaceKey}/property/{key}                    |       |
|PUT        |/rest/space/{spaceKey}/property/{key}                    |       |
|DELETE     |/rest/space/{spaceKey}/property/{key}                    |       |
|POST       |/rest/space/{spaceKey}/property/{key}                    |       |

## user

| HTTP Type | Endpoint                                                | State |
|-----------|--------------------------------------------------------:|-------|
|GET        |/rest/user                                               | 1     |
|GET        |/rest/user/anonymous                                     | 1     |
|GET        |/rest/user/current                                       | 1     |
|GET        |/rest/user/memberof                                      | 1     |

### user/watch

| HTTP Type | Endpoint                                                | State |
|-----------|--------------------------------------------------------:|-------|
|POST       |/rest/user/watch/content/{contentId}                     | 1     |
|DELETE     |/rest/user/watch/content/{contentId}                     | 1     |
|GET        |/rest/user/watch/content/{contentId}                     | 1     |
|POST       |/rest/user/watch/space/{spaceKey}                        | 1     |
|DELETE     |/rest/user/watch/space/{spaceKey}                        | 1     |
|GET        |/rest/user/watch/space/{spaceKey}                        | 1     |
