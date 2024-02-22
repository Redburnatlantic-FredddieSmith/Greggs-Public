import googlemaps
import pandas as pd

# api key needs billing info to work
api_key = 'AIzaSyAwFD9ovXIgPaavhP533qa2XpWE6IINzf0'
gmaps = googlemaps.Client(key=api_key)

def find_greggs_stores_from_csv(csv_file):
    df = pd.read_csv(csv_file)

    place_ids = []

    for index, row in df.iterrows():
        lat, lng = row['Latitude'], row['Longitude']

        # Perform a Places API request using the exact coordinates
        places_result = gmaps.places(query='Greggs', location=(lat, lng), type='bakery')

        for place in places_result['results']:
            place_ids.append(place['place_id'])

    return place_ids

def get_opening_and_closing_hours(place_id):
    place_details = gmaps.place(place_id=place_id, fields=['name', 'opening_hours'])

    if 'opening_hours' in place_details['result']:
        opening_hours = place_details['result']['opening_hours']['weekday_text']
        
        # Extract closing hours from the last entry in the 'weekday_text' list
        closing_hours = opening_hours[-1]

        return opening_hours, closing_hours
    else:
        return "Opening hours not available.", "Closing hours not available."

def main():
    csv_file_path = '/workspaces/Greggs-Public/GRGS_CSV.csv'
    
    greggs_place_ids = find_greggs_stores_from_csv(csv_file_path)

    data = {'Place ID': [], 'Opening Hours': [], 'Closing Hours': []}

    for place_id in greggs_place_ids:
        data['Place ID'].append(place_id)
        opening_hours, closing_hours = get_opening_and_closing_hours(place_id)
        data['Opening Hours'].append(opening_hours)
        data['Closing Hours'].append(closing_hours)

    df = pd.DataFrame(data)

    # Save data to an Excel file
    df.to_excel('/workspaces/Greggs-Public/output.xls', index=False)

if __name__ == "__main__":
    main()