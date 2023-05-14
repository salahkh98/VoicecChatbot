from django.conf import settings
from django.shortcuts import render
import openai
from .models import Conversation , NetworkProblem
import speech_recognition as sr
from rest_framework.decorators import api_view
from rest_framework.response import Response
from langdetect import detect
from django.db.models import Q
from pyarabic.araby import strip_tashkeel


openai.api_key = settings.OPENAI_API_KEY


model_engine = "text-davinci-002"
gpt2_model = "text-davinci-002"



@api_view(['POST'])
def chatbot(request):
    user_message = request.data.get('message')
    lang_code = detect(user_message)

    if user_message == 'مرحبا':
        chatbot_response = 'أهلاً بك! كيف يمكنني مساعدتك اليوم؟'
    else:
        # Retrieve the relevant network problems
        network_problems = NetworkProblem.objects.filter(
            Q(problem__icontains=user_message) | Q(problem__icontains=strip_tashkeel(user_message)) | Q(problem__icontains=lang_code)
        )

        # Generate the prompt for OpenAI's GPT-2
        prompt = f"{user_message}\nBot: "

        for problem in network_problems:
            # Get the solution in the same language as the user's input
            if lang_code == 'en':
                solution = problem.solution.split('\n')[1]
            elif lang_code == 'ar':
                solution = problem.solution.split('\n')[0]
            else:
                solution = problem.solution

            # Append the problem and solution to the prompt
            prompt += f"المشكلة:{problem.problem}\الحل: {solution}\n"
            
            
        completions = openai.Completion.create(
            engine=gpt2_model,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            best_of=1,


        )

        chatbot_response = completions.choices[0].text.strip()


    chatbot_response = chatbot_response.replace('Bot: ', '').replace('المشكلة:', '').replace('الحل:', '').replace('User:' , '')
    return Response({'response': chatbot_response})

def chat(request):
    conversations = Conversation.objects.all()
    return render(request, 'chat.html', {'conversations': conversations})