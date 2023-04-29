import fetch from "node-fetch";

export default async function handler(req, res) {
    const { photo_reference } = req.query;
    const apiKey = process.env.GOOGLE_MAPS_API_KEY;

    const url = `https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=${photo_reference}&key=${apiKey}`;

    try {
        const response = await fetch(url);

        if (response.ok) {
            res.setHeader("Content-Type", response.headers.get("Content-Type"));
            response.body.pipe(res);
        } else {
            console.error(`Unexpected response ${response.statusText}`);
            res.status(response.status).end();
        }
    } catch (error) {
        console.error(error);
        res.status(500).end();
    }
};