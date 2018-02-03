from confluence.models.auditrecord import AuditRecord
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def test_create_audit_record(): 
    a = AuditRecord({
        "author":  {
            "type":  "user",
            "displayName": "A Name",
            "username": "an",
            "userKey": "1"
        },
        "remoteAddress": "1.1.1.1,2.2.2.2",
        "creationDate": 1517497826248,
        "summary": "Space Workflow States Initialized",
        "description": "",
        "category": "Comala Workflows",
        "sysAdmin": True,
        "affectedObject": {
            "name": "About",
            "objectType": "Space"
        },
        "changedValues": [{
            "name": "stateName",
            "oldValue": "",
            "newValue": "Up to date"
        }, {
            "name": "overrideCurrentState",
            "oldValue": "",
            "newValue": "false"
        }],
        "associatedObjects": []
    })

    assert str(a) == 'Space Workflow States Initialized'
    assert '1.1.1.1' in a.remote_address and '2.2.2.2' in a.remote_address
    assert len(a.changed_values) == 2
    assert a.creation_date.strftime('%Y-%m-%d') == '2018-02-01'
