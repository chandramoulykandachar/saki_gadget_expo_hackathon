import pickle
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from saki.models import User, App
from sakiML.transitions_meets_tensorflow import ActivityClassifier
from saki.serializers import UserSerializer, AppSerializer, PredictionSerializer, TrainSerializer


class Users(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        """
        Get a list of all the users.
        :param request: /?master=master is mandatory
        :param format:
        :return:
        """

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Add a new user.
        :param request: /?master=master is mandatory
        :param format:
        :return:
        """
        if request.query_params['master'] == 'master':
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "invalid user"}, status=status.HTTP_400_BAD_REQUEST)


class Apps(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        """
        Get a list of all the apps for the given user
        :param request: /?api_key=<the api key>&user_name=<the user name>
        :param format:
        :return:
        """
        if request.query_params['api_key'] == User.objects.all().filter(user_name=request.query_params['user_name'])[
            0].api_key:
            user = App.objects.all().filter(user=User.objects.all().filter(user_name=request.query_params['user_name'])[0])
            serializer = AppSerializer(user, many=True)
            print serializer
            return Response(serializer.data)
        else:
            return Response({"error": "invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, format=None):
        """
        Add a new app to your account

        :param request:
        :param format:
        :return:
        """
        if request.query_params['api_key'] == User.objects.all().filter(user_name=request.query_params['user_name'])[
            0].api_key:
            serializer = AppSerializer(User.objects.all().filter(user_name=request.query_params['user_name'])[0],
                                       data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "invalid user"}, status=status.HTTP_400_BAD_REQUEST)


class Prediction(APIView):
    """
    List all snippets, or create a new snippet.

    t = ActivityClassifier('com_dark_candycab')
    t.train()
    t.transition('BookingActivity',
                 'My pick up location is basvangudi and my drop location is tyagrajnagara. book a cab and call the driver.')

    """

    def get(self, request, format=None):
        return Response({"response": "lol fail"}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Add a new user.
            :param request: /?master=master is mandatory
        :param format:
        :return:
        """
        if request.query_params['api_key'] == User.objects.all().filter(user_name=request.query_params['user_name'])[
            0].api_key:

            serializer = PredictionSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    trained_object = pickle.load(
                        open(request.query_params['user_name'] + '_' + serializer.validated_data['app_name'] + '.pickle', "rb"))
                    print serializer.validated_data
                    x = trained_object.transition(serializer.validated_data['current_activity'],
                                                  serializer.validated_data['message'])
                    print "here"
                    print x
                except Exception as e:
                    print e
                    return Response({"error": "The current model not trained"}, status=status.HTTP_204_NO_CONTENT)
                return Response(x, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "invalid user"}, status=status.HTTP_400_BAD_REQUEST)


class Train(APIView):
    """
    List all snippets, or create a new snippet.

    t = ActivityClassifier('com_dark_candycab')
    t.train()
    t.transition('BookingActivity',
                 'My pick up location is basvangudi and my drop location is tyagrajnagara. book a cab and call the driver.')

    """

    def get(self, request, format=None):
        return Response({"response": "lol fail"}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Add a new user.
        :param request: /?master=master is mandatory
        :param format:
        :return:
        """
        if request.query_params['api_key'] == User.objects.all().filter(user_name=request.query_params['user_name'])[
            0].api_key:
            serializer = TrainSerializer(data=request.data)
            if serializer.is_valid():
                ac = ActivityClassifier(serializer.validated_data['app_name'])
                ac.train(request.query_params['user_name'])
                return Response({"response": "successfully trained"}, status=status.HTTP_201_CREATED)
            return Response({"error": "couldn't train the classifier"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "invalid user"}, status=status.HTTP_400_BAD_REQUEST)