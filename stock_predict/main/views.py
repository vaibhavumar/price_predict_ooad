from django.shortcuts import render
from .forms import home_form
from django.contrib import messages
from django.views.generic import TemplateView
from .OOAD import predict_price
# Create your views here.

class homepage(TemplateView):
	template_name = "main/home.html"

	def get(self, request):
		form = home_form()
		return render(request,"main/home.html",context={"form":form})

	def post(self, request):
		# messages.info(request, f"RUNNING MODEL. Please Wait...")
		form = home_form(request.POST)
		if form.is_valid():
			date = form.cleaned_data['date']
			price, actual = predict_price(date)
			if price==-1:
				messages.error(request, f"ERROR: {actual}")
				return render(request,"main/home.html",context={"form":form})
			else:
				form = home_form()
				return render(request,"main/home.html",context={"form":form, "price": price, "actual": actual, "date":date})