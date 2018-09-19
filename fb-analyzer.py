import csv
import os
import json
import numpy as np
import pylab as pl
import datetime

CURRENT_DIRECTORY = os.getcwd()
NUMBER_TO_ANALYZE = 5000
MESSAGE_THRESHOLD = 1000

def get_json_data(final_chat):
	try:
		json_location = CURRENT_DIRECTORY + "/messages/" + final_chat + "/message.json"
		with open(json_location) as json_file:
			json_data = json.load(json_file)
			return json_data
	except:
		print(final_chat)

all_chats = os.listdir(CURRENT_DIRECTORY + "/messages")
final_chats = all_chats[:NUMBER_TO_ANALYZE]
sorted_final_chats = []
final_data_messages = {}
final_data_times = {}
final_data_words = {}

print('Analyzing ' + str(NUMBER_TO_ANALYZE) + ' chats...')

for final_chat in final_chats:
	if final_chat != "stickers_used":
		json_data = get_json_data(final_chat)
		messages = json_data["messages"]
		if len(messages) >= MESSAGE_THRESHOLD:
			sorted_final_chats.append((len(messages), final_chat, messages))

print('Finished reading in chats...')

sorted_final_chats.sort(reverse=True)

for i, (messages, final_chat, messages) in enumerate(sorted_final_chats):
	number_messages = {}
	person_to_times = {}
	number_words = {}
	
	#participants = [person["name"] for person in json_data["participants"]]
	
	for message in messages:
		try:
			name = message["sender_name"]
			number_messages[name] = number_messages.get(name, 0)
			number_messages[name] += 1

			time = message["timestamp_ms"]
			person_to_times[name] = person_to_times.get(name, [])
			person_to_times[name].append(datetime.datetime.fromtimestamp(time/1000.0))

			message_content = message["content"]
			number_words[name] = number_words.get(name, [])
			number_words[name].append(len(message_content.split()))
		except KeyError:
			pass
	print(str(i) + " - " + str(len(messages)) + " messages - " + str(final_chat))
	final_data_messages[i] = number_messages
	final_data_times[i] = person_to_times
	final_data_words[i] = number_words

def plot_num_messages(chat_number):
    plotted_data = final_data_messages[chat_number]
    X = np.arange(len(plotted_data))
    pl.bar(X, list(plotted_data.values()), align='center', width=0.5, color = 'r', bottom = 0.3)
    pl.xticks(X, plotted_data.keys(), rotation = 90)
    pl.title('Number of Messages Sent')
    pl.tight_layout()
    pl.show()

def plot_histogram_time(chat_number):
	person_to_times = final_data_times[chat_number]
	pl.xlabel('Time')
	pl.ylabel('Number of Messages')
	pl.title('# of Messages Over Time')
	colors = ['b', 'r', 'c', 'm', 'y', 'k', 'w', 'g']
	for i , person in enumerate(person_to_times):
		plotted_data = person_to_times[person]
		pl.hist(plotted_data, 100, alpha=0.3, label=person, facecolor=colors[i % len(colors)])
	pl.tight_layout()
	pl.legend()
	pl.show()

def plot_histogram_words(chat_number):
	temp = {}
	for person in final_data_words[chat_number]:
		temp[person] = np.average(final_data_words[chat_number][person])
	plotted_data = temp
	X = np.arange(len(plotted_data))
	pl.bar(X, list(plotted_data.values()), align='center', width=0.5, color = 'r', bottom = 0.3)
	pl.xticks(X, plotted_data.keys(), rotation = 90)
	pl.title('Average Word Count')
	pl.tight_layout()
	pl.show()
	
plot_histogram_time(37)