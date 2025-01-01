import React, { useState } from "react";
import "./DefineCustomCategory.css"; // Updated styles

const DefineCustomCategory = ({ onAddCategory, onClose }) => {
  const [categoryName, setCategoryName] = useState("");
  const [categoryNames, setCategoryNames] = useState([]);

  const handleAddCategory = () => {
    if (categoryName.trim()) {
      setCategoryNames([...categoryNames, categoryName.trim()]); // Add trimmed category
      setCategoryName(""); // Clear input field
    }
  };

  const handleSaveCategories = () => {
    if (categoryNames.length > 0) {
      onAddCategory([...categoryNames]); // Pass the array correctly
      onClose(); // Close modal
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-rectangle">
        <h2 className="modal-title">Define Custom Category</h2>
        <div className="modal-input-container">
          <input
            type="text"
            value={categoryName}
            placeholder="Name"
            onChange={(e) => setCategoryName(e.target.value)}
            className="modal-input"
          />
          <button onClick={handleAddCategory} className="add-button">
            ➕
          </button>
        </div>

        {/* Display added categories as cards */}
        <div className="category-cards">
          {categoryNames.map((category, index) => (
            <div key={index} className="category-card">
              {category}
            </div>
          ))}
        </div>

        <button onClick={handleSaveCategories} className="close-button">
          ✔️
        </button>
      </div>
    </div>
  );
};

export default DefineCustomCategory;
