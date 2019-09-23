def bot_bio_filter(user):
  bot = ['iamabot', 'imabot', 'justabot']

  # description has whitespace removed and downcased
  bot_bio = ''.join(user['description'].split(' ')).lower()
  
  if any(x in bot_bio for x in bot):
    return True
  else:
    return False

#def test_filter():
#  users = retrieve_users()
#  res = {}
#  for user in users:
#    res[user['id']] = bot_bio_filter(user)
#
#  print(res)
#
#test_filter()
