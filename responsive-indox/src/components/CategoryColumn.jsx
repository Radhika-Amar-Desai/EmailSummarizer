import React from "react";

const CategoryColumn = ({ title, cards, bgColor }) => {
  return (
    <div
      style={{
        backgroundColor: bgColor,
        padding: "10px",
        borderRadius: "0px",
        width: "20%",
        minHeight: "200px",
      }}
    >
      <div
        style={{
          backgroundColor: bgColor,
          padding: "5px 15px",
          borderRadius: "0px",
          display: "inline-block",
          marginBottom: "30px",
        }}
      >
        <h3 style={{ margin: 0, fontFamily: "Inter, sans-serif" }}>{title}</h3>
      </div>
      
      <div style={{ 
        display: "grid",
        gridTemplateColumns: "repeat(2, 1fr)",
        gap: "5px",
        padding: "0 10px"
      }}>
        {cards.map((card, index) => (
          <div
            key={index}
            style={{
              backgroundColor: card.color,
              padding: "20px",
              borderRadius: "0px",
              height: "70px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              boxShadow: "0px 2px 4px rgba(0, 0, 0, 0.1)",
              fontFamily: "Inter, sans-serif",
              fontSize: "14px",
              color: "#fff",
            }}
          >
            {card.text}
          </div>
        ))}
      </div>
    </div>
  );
};

export default CategoryColumn;