
const mymap = L.map('issMap').setView([-26.2309, 28.0583], 13);
const attribution = '&copy <a href="https://www.openstreemap/copyright">OpenStreet</a>contrubutors';

const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

const tiles = L.tileLayer(tileUrl, { attribution });

tiles.addTo(mymap);
const api_url = 'https://api.wheretheiss.at/v1/satellites/25544';

async function sucessCallback(position) {
    lat = position.coords.latitude;
    long = position.coords.longitude;

    // marker.setLatLng(lat,long)
    L.marker([lat, long]).addTo(mymap);

    data = { lat, long };
    const options = {
        headers: new Headers({
            'content-type': 'application/json'
        }),
        method: 'POST',
        body: JSON.stringify(data)
    }
    await fetch(`${window.origin}/profile`, options).then(response => {
        console.log(response)
        if (response.status !== 200) {
            console.log(`Your status is ${response.status} it's not 200`)

            return;
        }
    }).catch((reason) => {
        console.log(reason)

    })
}
async function fetching(error) {
    await fetch('https://ipapi.co/json/', {

        headers: new Headers({
            'content-type': 'application/json'
        })
    }).then(function (response) {
        console.log(response)

        if (response.status !== 200) {
            console.log(`Response status was not 200:${response.status}`)

            return;
        }
        response.json().then(function (data) {
            // console.log(data)
            lat = data.latitude,
                long = data.longitude,

                coordinates = { long, lat }
            fetch(`${window.origin}/profile`, {
                method: 'POST',
                credentials: 'include',
                body: JSON.stringify(coordinates),
                cache: 'no-cache',
                headers: new Headers({
                    'content-type': 'application/json'
                })
            }).then(function (response) {

                return;
            }).catch((reason) => {
                console.log(reason)
            })
            // response.json().then(function(data){
            // console.log(data)
        })


    })
}

if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(sucessCallback, fetching)
} else {
    console.log('HTML5 geolocation is unsuported')
}