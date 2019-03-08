import psycopg2
import requests
from groupy.client import Client

from credentials import GROUPME_URL, BOT_ID, GROUPME_TOKEN, POSTGRES_STRING

def sendMessage(content):
  params = {
    "bot_id"  : BOT_ID,
    "text"    : content
  }

  r = requests.post(url = GROUPME_URL + '/bots/post', params = params)

def messageToDB(message, conn):
  if(message.text != None):
    print(str(i) + ' : ' + str(message.created_at))
  else:
    message.text = ''
  try:
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (id, user_id, text, timestamp) VAlues ( %s, %s, %s, %s )", (str(message.id), str(message.user_id), str(message.text), str(message.created_at)) )
    print(cur.statusmessage)
  except Exception as e:
    print("Error Inserting message: " + str(e))
    print("USER_ID: " + str(message.user_id) + " NAME: " + str(message.name))
    print("ERRING MESSAGE: " + str(message.id) + str(message.user_id) + str(message.text) + str(message.created_at))
    exit()

def likesToDB(message, conn):
  likeslist = message.favorited_by
  if(likeslist != None):
    for liker in likeslist:
      try:
        cur = conn.cursor()
        cur.execute("INSERT INTO likes (user_id, message_id) VALUES ( %s, %s )", (str(liker), str(message.id)) )
        print(cur.statusmessage)
      except Exception as e:
        print("Error Uploading User: " + str(e))

def attachmentsToDB(message, conn):
  attachmentslist = message.attachments
  if(attachmentslist != None):
    for attachment in attachmentslist:
      if(attachment.type == 'image'):
        try:
          cur = conn.cursor()
          cur.execute("UPDATE messages SET image_url = %s WHERE id = %s", (str(attachment.url), str(message.id)) )
          print(cur.statusmessage)
        except Exception as e:
          print("Error Uploading User: " + str(e))

def groupMemberToDB(member, conn):
  try:
    cur = conn.cursor()
    cur.execute("INSERT INTO users (id, username) VALUES ( %s, %s )", (str(member.user_id), str(member.nickname)) )
    print(cur.statusmessage)
  except Exception as e:
    print("Error Uploading User: " + str(e))

def connectToPostgres():
  try:
    conn = psycopg2.connect(POSTGRES_STRING)
    print("connected")
    return conn
  except Exception as e:
    print("I am unable to connect to the database: " + str(e)) 

def getLastUploadedID():
  try:
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages WHERE id = ( SELECT MIN(id) FROM messages )")
    msg_list = cur.fetchone()
    return msg_list[0]

  except Exception as e:
    print("Error Executing Query: " + str(e))
  
def getLastUploadedIDLikes():
  try:
    cur = conn.cursor()
    cur.execute("SELECT * FROM likes WHERE message_id = ( SELECT MIN(message_id) FROM likes )")
    msg_list = cur.fetchone()
    return msg_list[1]

  except Exception as e:
    print("Error Executing Query: " + str(e))

def saveQueries(conn):
  try:
      conn = conn.commit()
      print("changes committed")

  except Exception as e:
      print("Commit Error: " + str(e))

if __name__ == '__main__':
  client = Client.from_token(GROUPME_TOKEN)

  conn = connectToPostgres()

  curr_id = getLastUploadedIDLikes()
  print(curr_id)

  for group in client.groups.list():
    if (group.name == 'Boys’ Club'):
      i=0
      '''
      for member in group.members:
        print(member.user_id, member.nickname)
        groupMemberToDB(member, conn)
      
      for message in group.messages.list_before(155201300435010501):
        likesToDB(message, conn)
        attachmentsToDB(message, conn)
        curr_id = message.id
        i+=1
      saveQueries(conn)
      '''
      while(curr_id != None):
        for message in group.messages.list_before(curr_id):
          print(i)
          likesToDB(message, conn)
          attachmentsToDB(message, conn)
          new_curr_id = message.id
          i+=1
        curr_id = new_curr_id
        saveQueries(conn)
  saveQueries(conn)

