import React, { useState } from 'react';
import './Filter.css';

const Filter = ({ onFilterChange }) => {
    const [showTeamOptions, setShowTeamOptions] = useState(false);
    const [showCountryOptions, setShowCountryOptions] = useState(false);
    const [showColorOptions, setShowColorOptions] = useState(false);
    const [showPriceOptions, setShowPriceOptions] = useState(false);

    const handleToggle = (setShowFunc) => {
        setShowFunc(prevState => !prevState);
    };

    return (
        <div className="filter-container">
            {/* Team Filter */}
            <div className="filter-category">
                <h4 onClick={() => handleToggle(setShowTeamOptions)}>Team</h4>
                <div className={`filter-options ${showTeamOptions ? 'active' : ''}`}>
                    <label>
                        <input type="checkbox" name="team" value="Chelsea F.C." onChange={onFilterChange} /> Chelsea F.C.
                    </label>
                    <label>
                        <input type="checkbox" name="team" value="S.C. Corinthians" onChange={onFilterChange} /> S.C. Corinthians
                    </label>
                    <label>
                        <input type="checkbox" name="team" value="England National Team" onChange={onFilterChange} /> England National Team
                    </label>
                    <label>
                        <input type="checkbox" name="team" value="Liverpool F.C." onChange={onFilterChange} /> Liverpool F.C.
                    </label>
                    <label>
                        <input type="checkbox" name="team" value="F.C. Barcelona" onChange={onFilterChange} /> F.C. Barcelona
                    </label>
                    <label>
                        <input type="checkbox" name="team" value="Brazil National Team" onChange={onFilterChange} /> Brazil National Team
                    </label>
                    <label>
                        <input type="checkbox" name="team" value="Club América" onChange={onFilterChange} /> Club América
                    </label>
                    <label>
                        <input type="checkbox" name="team" value="Tottenham Hotspur" onChange={onFilterChange} /> Tottenham Hotspur
                    </label>
                </div>
            </div>

            {/* Country Filter */}
            <div className="filter-category">
                <h4 onClick={() => handleToggle(setShowCountryOptions)}>Country</h4>
                <div className={`filter-options ${showCountryOptions ? 'active' : ''}`}>
                    <label>
                        <input type="checkbox" name="country" value="England" onChange={onFilterChange} /> England
                    </label>
                    <label>
                        <input type="checkbox" name="country" value="Mexico" onChange={onFilterChange} /> Mexico
                    </label>
                    <label>
                        <input type="checkbox" name="country" value="Brazil" onChange={onFilterChange} /> Brazil
                    </label>
                    <label>
                        <input type="checkbox" name="country" value="Spain" onChange={onFilterChange} /> Spain
                    </label>
                </div>
            </div>

            {/* Color Filter */}
            <div className="filter-category">
                <h4 onClick={() => handleToggle(setShowColorOptions)}>Color</h4>
                <div className={`filter-options ${showColorOptions ? 'active' : ''}`}>
                    <label>
                        <input type="checkbox" name="color" value="Yellow" onChange={onFilterChange} /> Yellow
                    </label>
                    <label>
                        <input type="checkbox" name="color" value="Blue" onChange={onFilterChange} /> Blue
                    </label>
                    <label>
                        <input type="checkbox" name="color" value="Red" onChange={onFilterChange} /> Red
                    </label>
                    <label>
                        <input type="checkbox" name="color" value="Black" onChange={onFilterChange} /> Black
                    </label>
                    <label>
                        <input type="checkbox" name="color" value="White" onChange={onFilterChange} /> White
                    </label>
                    <label>
                        <input type="checkbox" name="color" value="Green" onChange={onFilterChange} /> Green
                    </label>
                    <label>
                        <input type="checkbox" name="color" value="Pink" onChange={onFilterChange} /> Pink
                    </label>
                    <label>
                        <input type="checkbox" name="color" value="Grey" onChange={onFilterChange} /> Grey
                    </label>
                    <label>
                        <input type="checkbox" name="color" value="Purple" onChange={onFilterChange} /> Purple
                    </label>
                    <label>
                        <input type="checkbox" name="color" value="Brown" onChange={onFilterChange} /> Brown
                    </label>
                </div>
            </div>

            {/* Price Filter */}
            <div className="filter-category">
                <h4 onClick={() => handleToggle(setShowPriceOptions)}>Price Range</h4>
                <div className={`filter-options ${showPriceOptions ? 'active' : ''}`}>
                    <label>
                        <input type="checkbox" name="price" value="0-50" onChange={onFilterChange} /> £0 - £50
                    </label>
                    <label>
                        <input type="checkbox" name="price" value="50-100" onChange={onFilterChange} /> £50 - £100
                    </label>
                    <label>
                        <input type="checkbox" name="price" value="100-150" onChange={onFilterChange} /> £100 - £150
                    </label>
                </div>
            </div>
        </div>
    );
};

export default Filter;
