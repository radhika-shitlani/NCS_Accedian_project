from pprint import pprint
list1 = [[{'stream_id': 'streamblock1', 'status': '1'}, {'stream_id': 'streamblock2', 'status': '1'}], [{'stream_id': 'streamblock3', 'status': '1'}, {'stream_id': 'streamblock4', 'status': '1'}]]
print(len(list1))
print(len(list1[0]))
for i in range(len(list1[0])):
    pprint(list1[0][i])
    pprint(list1[1][i])
    pprint('!!!!!!!!!!!')