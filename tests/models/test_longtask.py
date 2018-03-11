from confluence.models.longtask import LongTask
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def test_create_full_json():
    t = LongTask({
        "id": "14365eab-f2df-4ecb-9458-75ad3af903a7",
        "name": {
            "key": "com.atlassian.confluence.extra.flyingpdf.exporttaskname",
            "args": []},
        "elapsedTime": 101770,
        "percentageComplete": 100,
        "successful": True,
        "messages": [{
            "translation": "Finished PDF space export. Download <a "
                           "href=\"/confluence/download/temp/pdfexport-20180111-110118-1209-23/x-110118-1209-24.pdf"
                           "\">here</a>.",
            "args": []
        }]
    })

    assert str(t) == 'com.atlassian.confluence.extra.flyingpdf.exporttaskname'
    assert len(t.messages) == 1
    assert t.successful
