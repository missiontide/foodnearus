const axios = require('axios');

export default async function handler(req, res) {
    const { latitude, longitude } = req.body;

    try {
        const apiKey = process.env.GOOGLE_MAPS_API_KEY;
        const response = await axios.get(`https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=${latitude},${longitude}&radius=1000&type=restaurant&key=${apiKey}`);
        const { results } = response.data;
        // res.status(200).json(response.data);
        const places = results.map((place) => {
            return {
                name: place.name,
                photoUrl: place.photos ? `https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=${place.photos[0].photo_reference}&key=${apiKey}` : '',
            };
        });
        res.status(200).json(places);
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Error fetching nearby restaurants.' });
    }
}