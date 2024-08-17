from django.contrib.auth.models import AbstractUser
from django.db import models

country_list = [(country, country) for country in [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua & Deps", 
    "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", 
    "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", 
    "Bhutan", "Bolivia", "Bosnia Herzegovina", "Botswana", "Brazil", "Brunei", 
    "Bulgaria", "Burkina", "Burundi", "Cambodia", "Cameroon", "Canada", 
    "Cape Verde", "Central African Rep", "Chad", "Chile", "China", "Colombia", 
    "Comoros", "Congo", "Congo {Democratic Rep}", "Costa Rica", "Croatia", "Cuba", 
    "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", 
    "Dominican Republic", "East Timor", "Ecuador", "Egypt", "El Salvador", 
    "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia", "Fiji", "Finland", 
    "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", 
    "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", 
    "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", 
    "Ireland {Republic}", "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan", 
    "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea North", "Korea South", 
    "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", 
    "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Macedonia", 
    "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", 
    "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", 
    "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", 
    "Myanmar, {Burma}", "Namibia", "Nauru", "Nepal", "Netherlands", 
    "New Zealand", "Nicaragua", "Niger", "Nigeria", "Norway", "Oman", "Pakistan", 
    "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", 
    "Poland", "Portugal", "Qatar", "Romania", "Russian Federation", "Rwanda", 
    "St Kitts & Nevis", "St Lucia", "Saint Vincent & the Grenadines", "Samoa", 
    "San Marino", "Sao Tome & Principe", "Saudi Arabia", "Senegal", "Serbia", 
    "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", 
    "Solomon Islands", "Somalia", "South Africa", "South Sudan", "Spain", 
    "Sri Lanka", "Sudan", "Suriname", "Swaziland", "Sweden", "Switzerland", 
    "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Togo", "Tonga", 
    "Trinidad & Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", 
    "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", 
    "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", 
    "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
]]

class User(AbstractUser):
    pass


class Location(models.Model):
    country = models.CharField(max_length=100, choices=country_list)

    def __str__(self):
        return f"{self.country}"
    

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"{self.location} ({self.start_date} to {self.end_date})"


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    date = models.DateField()
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Note on {self.date} by {self.user.username}"