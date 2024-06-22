import React, { useState } from 'react';

const GeoForm = ({ handleCoordinatesSubmit }) => {
  const [errors, setErrors] = useState({});
  const [latitude, setLatitude] = useState('');
  const [longitude, setLongitude] = useState('');
  const validateLatitude = (lat) => {
    const latNum = parseFloat(lat);
    if (isNaN(latNum) || latNum < -90 || latNum > 90) {
      return 'must be between -90 and 90.';
    }
    return '';
  };

  const validateLongitude = (lon) => {
    const lonNum = parseFloat(lon);
    if (isNaN(lonNum) || lonNum < -180 || lonNum > 180) {
      return 'must be between -180 and 180.';
    }
    return '';
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const latError = validateLatitude(latitude);
    const lonError = validateLongitude(longitude);

    if (latError || lonError) {
      setErrors({ latitude: latError, longitude: lonError });
    } else {
      setErrors({});
      handleCoordinatesSubmit(latitude, longitude)
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex">
      <div className="mr-[1rem]">
        <label>
          Latitude:
          <input
            type="number"
            value={latitude}
            onChange={(e) => setLatitude(e.target.value)}
            className="w-[3rem] ml-[1rem] rounded-lg"
          />
        </label>
        {errors.latitude && <div className="text-red-600 text-sm">{errors.latitude}</div>}
      </div>
      <div className="mr-[1rem]">
        <label>
          Longitude:
          <input
            type="number"
            value={longitude}
            onChange={(e) => setLongitude(e.target.value)}
            className="w-[3rem] ml-[1rem] rounded-lg"
          />
        </label>
        {errors.longitude && <div  className="text-red-600 text-sm">{errors.longitude}</div>}
      </div>
      <button className="pushable" type="submit"><span className="front px-5 py-2 text-base">OK</span></button>
    </form>
  );
};

export default GeoForm;
