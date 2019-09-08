from django.test import TestCase

# Create your tests here.
from datetime import datetime

dt = datetime.strptime("16 Nov, 2009", "%d %b, %Y")
print(dt.strftime("%Y-%m-%d"))