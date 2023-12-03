from flask import Flask, render_template, redirect, request,url_for
import requests
import json
app = Flask(__name__)

production = False


@app.route('/identify-plant', methods=['POST'])
def identify_plant():
    
    api={
        'url': 'https://plant.id/api/v3/identification',
        'key': 'WmvjWCEP3RuDeNQDxLS9MkgXsljLtS3xvehygJa75kUzBQr2ph',
    }
    
    if 'id_plant' in request.files:
        image_file = request.files.get('id_plant')
        if image_file.filename != '':
            try:
                api_url = api['url']
                headers = {'Api-Key': api['key']}                
                files = {'images': (image_file.filename, image_file.read())}
                params = {'details':'common_names,url,description,image,edible_parts,watering,propagation_methods'}

                if production:
                    response = requests.post(api_url, headers=headers, files=files, params=params)
                    response.raise_for_status()
                    result = response.json()

                else:
                    result =  json.load(open('plant_response.json', 'r'))
                    
                # with open('plant_response.json', 'w+')as file:
                #     json.dump(result, file)
                
                plant = result['result']['is_plant']['binary']
                
                if not plant:
                    return redirect(url_for('index',notify=True))
                
                propagation = result['result']['classification']['suggestions'][0]['details']['propagation_methods']             
                watering = result['result']['classification']['suggestions'][0]['details']['watering']                    
                edible_parts = result['result']['classification']['suggestions'][0]['details']['edible_parts']             
                image = result['result']['classification']['suggestions'][0]['details']['image']['value']            
                url = result['result']['classification']['suggestions'][0]['details']['url']            
                common_names = result['result']['classification']['suggestions'][0]['details']['common_names']            
                description = result['result']['classification']['suggestions'][0]['details']['description']['value']          
                plant_name = result['result']['classification']['suggestions'][0]['name']
                confidence = result['result']['classification']['suggestions'][0]['probability']
                
                common_names = ", ".join(common_names[:2])

                
                return redirect(url_for('result_plant',watering=watering,propagation=propagation,edible_parts=edible_parts,image=image,url=url,common_names=common_names,description=description,plant_name=plant_name,confidence=confidence)
)
            
            except requests.exceptions.RequestException as e:
                return redirect(url_for('result_plant', error=f"Error during API request. {e}"))
    
    return redirect(url_for('result_plant', error=f"Image not provided.{request.files}"))



@app.route('/identify-disease', methods=['POST'])
def identify_disease():
    
    api={
        'url': 'https://plant.id/api/v3/health_assessment',
        'key': 'WmvjWCEP3RuDeNQDxLS9MkgXsljLtS3xvehygJa75kUzBQr2ph',
    }
    
    if 'id_disease' in request.files:
        image_file = request.files.get('id_disease')
        if image_file.filename != '':
            try:
                api_url = api['url']               
                headers = {'Api-Key': api['key']}                
                files = {'images': (image_file.filename, image_file.read())}
                params = {'details':'local_name,description,url,treatment,classification,common_names,cause'}

                if production:
                    response = requests.post(api_url, headers=headers, files=files, params=params)
                    response.raise_for_status()
                    result = response.json()

                else:
                    result =  json.load(open('disease_response.json', 'r'))


                plant = result['result']['is_plant']['binary']
                
                if not plant:
                    return redirect(url_for('index',notify=True))


                image = result['input']['images'][0]
                is_healthy = result['result']['is_healthy']['binary']
                name = result['result']['disease']['suggestions'][0]["name"]
                probability = result['result']['disease']['suggestions'][0]["probability"]
                local_name = result['result']['disease']['suggestions'][0]["details"]["local_name"]
                description = result['result']['disease']['suggestions'][0]["details"]["description"]
                url = result['result']['disease']['suggestions'][0]["details"]["url"]
                biological_t = result['result']['disease']['suggestions'][0]["details"]["treatment"]["biological"]
                prevention_t = result['result']['disease']['suggestions'][0]["details"]["treatment"]["prevention"]
                cause = result['result']['disease']['suggestions'][0]["details"]["cause"]
                common_names = result['result']['disease']['suggestions'][0]["details"]["common_names"]
                classification = result['result']['disease']['suggestions'][0]["details"]["classification"]
                  
                
                prevention_t = " ".join(prevention_t)
                biological_t = " ".join(biological_t)
                classification = ", ".join(classification)
                
                
                return redirect(url_for('result_disease',image=image,is_healthy=is_healthy,name=name,probability=probability,local_name=local_name,description=description,url=url,biological_t=biological_t,prevention_t=prevention_t,cause=cause,common_names=common_names,classification=classification))

            except requests.exceptions.RequestException as e:
                return redirect(url_for('result_disease', error=f"Error during API request. {e}"))
    
    return redirect(url_for('result_disease', error=f"Image not provided.{request.files}"))


@app.route('/result-plant')
def result_plant():
    error =  request.args.get('error', '')
    image = request.args.get('image', 'N/A')
    url = request.args.get('url', 'N/A')
    description = request.args.get('description', 'N/A')
    description = request.args.get('description', 'N/A')
    
    details={
            "Confidence": request.args.get('confidence', 'N/A') ,
            "Common Names": request.args.get('common_names', 'Unknown Plant'),
            "Scientific Names": request.args.get('plant_name', 'N/A'),
            "Water (times a day)": request.args.get('watering', 'N/A'),
            "Propagation": request.args.get('propagation', 'N/A'),
            "Edible Parts":  request.args.get('edible_parts', 'N/A'),
        }
    
    
    return render_template('result.html', details=details,image=image,url=url,description=description)

@app.route('/result-disease')
def result_disease():
    error =  request.args.get('error', '')
    image = request.args.get('image', 'N/A')
    url = request.args.get('url', 'N/A')
    
    description={
                "Description":request.args.get('description', 'N/A'),
                "Biological_Treatment":request.args.get('biological_t', 'N/A'), 
                "Prevention":request.args.get('prevention_t', 'N/A'),
        }
    
    details={
            "Healthy": request.args.get('is_healthy', 'N/A') ,
            "Disease Names": request.args.get('name', 'Unknown Plant'),
            "Disease Common Name": request.args.get('common_names', 'N/A'),
            "Disease Probability": request.args.get('probability', 'N/A'),
            "Disease Classification": request.args.get('classification', 'N/A'),
            "Cause":  request.args.get('cause', 'N/A'),
        }
    
    
    return render_template('result.html', details=details,image=image,url=url,description=description)

@app.route('/', methods=['POST','GET'])
def index(data=0):
    notify =  request.args.get('notify', None)
    return render_template('index.html',notify=notify)


@app.route('/about')
def about():
    return render_template('about.html')




if __name__=='__main__':
    app.run(host='0.0.0.0', debug=False)
