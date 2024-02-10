from src.config import settings


admin_data = {
    "email": "admin@admin.com",
    "first_name": "Admin",
    "last_name": "Admin",
    "hashed_password": settings.ADMIN_PASSWORD,
    "role_id": 2,
    "is_superuser": True,
}

roles_data = [
    {"name": "user"},
    {"name": "admin"},
    {"name": "manager"},
]

countries_data = [
    {"name": "Aruba"},
    {"name": "Afghanistan"},
    {"name": "Angola"},
    {"name": "Albania"},
    {"name": "Andorra"},
    {"name": "United Arab Emirates"},
    {"name": "Argentina"},
    {"name": "Armenia"},
    {"name": "Antigua and Barbuda"},
    {"name": "Australia"},
    {"name": "Austria"},
    {"name": "Azerbaijan"},
    {"name": "Burundi"},
    {"name": "Belgium"},
    {"name": "Benin"},
    {"name": "Burkina Faso"},
    {"name": "Bangladesh"},
    {"name": "Bulgaria"},
    {"name": "Bahrain"},
    {"name": "Bahamas"},
    {"name": "Bosnia and Herzegovina"},
    {"name": "Belarus"},
    {"name": "Belize"},
    {"name": "Bermuda"},
    {"name": "Bolivia"},
    {"name": "Brazil"},
    {"name": "Barbados"},
    {"name": "Bhutan"},
    {"name": "Botswana"},
    {"name": "Central African Republic"},
    {"name": "Canada"},
    {"name": "Switzerland"},
    {"name": "Chile"},
    {"name": "China"},
    {"name": "Cameroon"},
    {"name": "Congo"},
    {"name": "Cook Island"},
    {"name": "Colombia"},
    {"name": "Comoros"},
    {"name": "Costa Rica"},
    {"name": "Cuba"},
    {"name": "Christmas Island"},
    {"name": "Cayman Islands"},
    {"name": "Cyprus"},
    {"name": "Czech_Republic"},
    {"name": "Germany"},
    {"name": "Djibouti"},
    {"name": "Dominica"},
    {"name": "Denmark"},
    {"name": "Dominican"},
    {"name": "Algeria"},
    {"name": "Ecuador"},
    {"name": "Egypt"},
    {"name": "Eritrea"},
    {"name": "Western"},
    {"name": "Spain"},
    {"name": "Estonia"},
    {"name": "Ethiopia"},
    {"name": "Finland"},
    {"name": "Fiji"},
    {"name": "Falkland Islands (Malvinas)"},
    {"name": "France"},
    {"name": "Faroe Islands"},
    {"name": "Micronesia"},
    {"name": "Gabon"},
    {"name": "United Kingdom"},
    {"name": "Georgia"},
    {"name": "Guernsey"},
    {"name": "Ghana"},
    {"name": "Gibraltar"},
    {"name": "Guinea"},
    {"name": "Guadeloupe"},
    {"name": "Gambia"},
    {"name": "Equatorial Guinea"},
    {"name": "Grenada"},
    {"name": "Guatemala"},
    {"name": "Guam"},
    {"name": "Hong Kong"},
    {"name": "Honduras"},
    {"name": "Croatia"},
    {"name": "Haiti"},
    {"name": "Hungary"},
    {"name": "Indonesia"},
    {"name": "India"},
    {"name": "Ireland"},
    {"name": "Iran"},
    {"name": "Iraq"},
    {"name": "Iceland"},
    {"name": "Israel"},
    {"name": "Italy"},
    {"name": "Jamaica"},
    {"name": "Jersey"},
    {"name": "Jordan"},
    {"name": "Japan"},
    {"name": "Kazakhstan"},
    {"name": "Kenya"},
    {"name": "Kyrgyzstan"},
    {"name": "Cambodia"},
    {"name": "Kiribati"},
    {"name": "Korea"},
    {"name": "Kuwait"},
    {"name": "Lebanon"},
    {"name": "Liberia"},
    {"name": "Libya"},
    {"name": "Saint Lucia"},
    {"name": "Liechtenstein"},
    {"name": "Sri Lanka"},
    {"name": "Lesotho"},
    {"name": "Marshall Islands"},
    {"name": "North Macedonia"},
    {"name": "New Zealand"},
    {"name": "Lithuania"},
    {"name": "Luxembourg"},
    {"name": "Latvia"},
    {"name": "Macao"},
    {"name": "Morocco"},
    {"name": "Monaco"},
    {"name": "Moldova"},
    {"name": "Madagascar"},
    {"name": "Maldives"},
    {"name": "Mexico"},
    {"name": "Mali"},
    {"name": "Malta"},
    {"name": "Myanmar"},
    {"name": "Montenegro"},
    {"name": "Mongolia"},
    {"name": "Mozambique"},
    {"name": "Mauritania"},
    {"name": "Montserrat"},
    {"name": "Martinique"},
    {"name": "Mauritius"},
    {"name": "Malawi"},
    {"name": "Malaysia"},
    {"name": "Mayotte"},
    {"name": "Namibia"},
    {"name": "Niger"},
    {"name": "Nigeria"},
    {"name": "Nicaragua"},
    {"name": "Niue"},
    {"name": "Netherlands"},
    {"name": "Norway"},
    {"name": "Nepal"},
    {"name": "Nauru"},
    {"name": "Oman"},
    {"name": "Pakistan"},
    {"name": "Pitcairn"},
    {"name": "Philippines"},
    {"name": "Panama"},
    {"name": "Peru"},
    {"name": "Palau"},
    {"name": "Papua New Guinea"},
    {"name": "Puerto Rico"},
    {"name": "Saudi_Arabia"},
    {"name": "Solomon Islands"},
    {"name": "Sierra Leone"},
    {"name": "El Salvador"},
    {"name": "San Marino"},
    {"name": "United States"},
    {"name": "Wallis and Futuna"},
    {"name": "Virgin Islands"},
    {"name": "South Africa"},
    {"name": "Poland"},
    {"name": "Portugal"},
    {"name": "Paraguay"},
    {"name": "Palestine"},
    {"name": "Qatar"},
    {"name": "Romania"},
    {"name": "Russia"},
    {"name": "Rwanda"},
    {"name": "Sudan"},
    {"name": "Senegal"},
    {"name": "Singapore"},
    {"name": "Somalia"},
    {"name": "Serbia"},
    {"name": "South Sudan"},
    {"name": "Suriname"},
    {"name": "Slovenia"},
    {"name": "Sweden"},
    {"name": "Eswatini"},
    {"name": "Seychelles"},
    {"name": "Chad"},
    {"name": "Togo"},
    {"name": "Thailand"},
    {"name": "Tajikistan"},
    {"name": "Tokelau"},
    {"name": "Turkmenistan"},
    {"name": "Tonga"},
    {"name": "Tunisia"},
    {"name": "Turkey"},
    {"name": "Tuvalu"},
    {"name": "Taiwan"},
    {"name": "Tanzania"},
    {"name": "Uganda"},
    {"name": "Ukraine"},
    {"name": "Uruguay"},
    {
        "name": "Uzbekistan",
    },
    {
        "name": "Venezuela",
    },
    {
        "name": "Vietnam",
    },
    {
        "name": "Vanuatu",
    },
    {
        "name": "Samoa",
    },
    {
        "name": "Yemen",
    },
    {
        "name": "Zambia",
    },
    {
        "name": "Zimbabwe",
    },
]

payment_types_data = [{"name": "Card"}]

product_categories_data = [
    {
        "name": "Man",
    },
    {"name": "Woman"},
    {"name": "Accessories"},
]

product_sub_categories_data = [
    {"name": "Tops", "parent_category_id": 1},
    {"name": "Bottoms", "parent_category_id": 1},
    {"name": "Outerwear", "parent_category_id": 1},
    {"name": "Tops", "parent_category_id": 2},
    {"name": "Dresses", "parent_category_id": 2},
    {"name": "Bottoms", "parent_category_id": 2},
    {"name": "Hats", "parent_category_id": 3},
    {"name": "Bags", "parent_category_id": 3},
    {"name": "Belts", "parent_category_id": 3},
]

product_sub_sub_categories_data = [
    {"name": "T-shirts", "parent_category_id": 4},
    {"name": "Shorts", "parent_category_id": 4},
    {"name": "Sweaters", "parent_category_id": 4},
    {"name": "Jeans", "parent_category_id": 5},
    {"name": "Pants", "parent_category_id": 5},
    {"name": "Shorts", "parent_category_id": 5},
    {"name": "Sweatpants", "parent_category_id": 5},
    {"name": "Jackets", "parent_category_id": 6},
    {"name": "Coats", "parent_category_id": 6},
    {"name": "Blazers", "parent_category_id": 6},
    {"name": "Blouses", "parent_category_id": 7},
    {"name": "T-shirts", "parent_category_id": 7},
    {"name": "Sweaters", "parent_category_id": 7},
    {"name": "Casual", "parent_category_id": 8},
    {"name": "Evening", "parent_category_id": 8},
    {"name": "Jeans", "parent_category_id": 9},
    {"name": "Pants", "parent_category_id": 9},
    {"name": "Skirts", "parent_category_id": 9},
    {"name": "Leggings", "parent_category_id": 9},
    {"name": "Baseball Caps", "parent_category_id": 10},
    {"name": "Beanines", "parent_category_id": 10},
    {"name": "Sun hats", "parent_category_id": 10},
    {"name": "Backpacks", "parent_category_id": 11},
    {"name": "Handbacks", "parent_category_id": 11},
    {"name": "Toge Bags", "parent_category_id": 11},
]
