import json
import _jsonnet

jsonnet_str = '''
{
  local OTHER_NAME = 'Bob',
  person1: {
    name: "Alice",
    welcome: "Hello " + self.name + "!",
  },
  person2: self.person1 {
    name: std.extVar("OTHER_NAME"),
  },
}
'''

json_str = _jsonnet.evaluate_snippet("snippet", jsonnet_str, ext_vars={'OTHER_NAME': 'Bob'})
# json_str = _jsonnet.evaluate_snippet("snippet", jsonnet_str)


json_obj = json.loads(json_str)
print(json_obj)
for person_id, person in json_obj.items():
    print('%s is %s, greeted by "%s"' % (person_id, person['name'], person['welcome']))