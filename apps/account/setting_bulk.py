from elasticsearch import Elasticsearch
import json

class elastic():
    def send():
        es = Elasticsearch("http://localhost:9200", timeout=300, max_retries=10, retry_on_timeout=True)

        es.indices.create(
            index='test',
            body={
                "settings": {
                    "index": {
                        "analysis": {
                            "analyzer": {
                                "my_analyzer": {
                                    "type": "custom",
                                    "tokenizer": "nori_tokenizer"
                                }
                            }
                        }
                    }
                },
                "mappings": {
                        "properties": {
                            "id": {
                                "type": "long"
                            },
                            "name": {
                                "type": "text",
                                "analyzer": "my_analyzer"
                            },
                            "info_company": {
                                "type": "text",
                                "analyzer": "my_analyzer"
                            },
                            "history": {
                                "type": "text",
                                "analyzer": "my_analyzer"
                            },
                            "category_middle": {
                                "type": "text",
                                "analyzer": "my_analyzer"
                            }
                        }
                }
            }
        )


        with open("/Users/iyuchang/Desktop/partner.json", encoding='utf-8') as json_file:
            json_data = json.loads(json_file.read())
        body = ""
        count = 1
        for i in json_data:
            body = body + json.dumps({"index": {"_index": "test", "_id": count}}) + '\n'
            body = body + json.dumps(i, ensure_ascii=False) + '\n'
            if count == 1:
                print(body)
            count += 1

        f = open('/Users/iyuchang/Desktop/input.json', 'w')
        f.write(body)
        f.close()

        es.bulk(body)
