import Head from 'next/head'
import Image from 'next/image'
import { Inter } from 'next/font/google'
import styles from '@/styles/Home.module.css'

const inter = Inter({ subsets: ['latin'] })

import { useState } from 'react';

function FoodPicker() {
    const [restaurants, setRestaurants] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleAllowLocation = () => {
        setIsLoading(true);
        setError(null);
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const { latitude, longitude } = position.coords;
                fetch(`/api/restaurants?lat=${latitude}&lng=${longitude}`)
                    .then((response) => response.json())
                    .then((data) => {
                        setRestaurants(data.results);
                        setIsLoading(false);
                    })
                    .catch((error) => {
                        setError(error.message);
                        setIsLoading(false);
                    });
            },
            (error) => {
                setError(error.message);
                setIsLoading(false);
            }
        );
    };

    return (
        <div>
            <h1>What should I eat?</h1>
            {!restaurants.length && (
                <div>
                    <button onClick={handleAllowLocation}>Allow Location</button>
                    {isLoading && <p>Loading...</p>}
                    {error && <p>{error}</p>}
                </div>
            )}
            {restaurants.length > 0 && (
                <div>
                    <h2>Choose a food:</h2>
                    <ul>
                        {restaurants.map((restaurant) => (
                            <li key={restaurant.place_id}>
                                {restaurant.name}
                                {restaurant.photos && (
                                    <img
                                        src={`/api/photo?photo_reference=${encodeURIComponent(restaurant.photos[0].photo_reference)}`}
                                        alt={`${restaurant.name} food`}
                                    />
                                )}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

export default FoodPicker;