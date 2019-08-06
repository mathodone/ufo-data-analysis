from django.shortcuts import render
from django.conf import settings
from rest_framework import views, status
from rest_framework.response import Response
from datetime import datetime, timedelta
import os
import pickle
import pandas as pd
import sklearn
import xgboost

# helper function
def format_datetime(raw_time: str) -> datetime:
    try:
        time = datetime.strptime(raw_time, "%m/%d/%Y %H:%M")
    # raised when 24:00
    except ValueError:
        time = raw_time.replace(' 24', ' 23')
        time = datetime.strptime(time, "%m/%d/%Y %H:%M")
        time += timedelta(hours = 1)

    return time

# Create your views here.
class Predict(views.APIView):
    # our POST prediction method
    def post(self, request):

        # load our model
        with open(os.path.join(settings.MODEL_ROOT, 'ufo_classifier.pkl'), 'rb') as file:
            classifier = pickle.load(file)
        try:
            # we need to edit the incoming data to work
            # with our classifier

            # check if passed datetime is formatted as described in readme
            try:
                formatted_datetime = format_datetime(request.data["datetime"])
            except Exception as e:
                return Response("Datetime needs to be properly formatted",status=status.HTTP_400_BAD_REQUEST)

            # check if duration an int. if not, make it an int
            try:
                formatted_duration = int(request.data["duration"])
            except Exception as e:
                return Response("Duration needs to be properly formatted",status=status.HTTP_400_BAD_REQUEST)

            # hour and month variables
            hour = formatted_datetime.hour
            month = formatted_datetime.month

            # night variable
            night = 0 if hour in range(6,17) else 1

            # create our dictionary of feature values
            # the scaler values are contained in arrays because that's
            # what pandas demands of us
            features = {
                "hour": [hour],
                "month": [month],
                "night": [night],
                "duration": [formatted_duration]
            }

            # create dataframe where we store our feature data
            obs_df = pd.DataFrame.from_dict(features)

            # we have to reorder our dataframe to have the
            # same order as the training set the classifier learned on
            obs_df = obs_df[["hour","month","night","duration"]]

            # return shape type as a string
            shapes = {
                0: "light",
                3: "round"
            }

            prediction = classifier.predict(obs_df)
            return Response({"shape": shapes[prediction[0]]}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)