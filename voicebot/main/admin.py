from django.contrib import admin
from .models import Conversation , NetworkProblem
# Register your models here.



class chatbotnetworkproblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'problem', 'solution')

admin.site.register(NetworkProblem , chatbotnetworkproblemAdmin)


class chatbotconversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_question', 'bot_response', 'created_at', 'updated_at')
    

admin.site.register(Conversation , chatbotconversationAdmin)


