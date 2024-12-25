import React from "react";
import NavBar from "./components/NavBar";
import CategoryColumn from "./components/CategoryColumn";

const App = () => {
  const categories = [
    {
      title: "Category-one",
      color: "#e0bbff", // Background color for the category column
      cards: Array(5).fill({ text: "wertrcyvu byi", color: "#b983ff" }), // Cards in the category
    },
    {
      title: "Category-two",
      color: "#bbffd0",
      cards: Array(4).fill({ text: "wertrcyvu byi", color: "#83ffa4" }),
    },
    {
      title: "Category-three",
      color: "#bbf0ff",
      cards: Array(5).fill({ text: "wertrcyvu byi", color: "#83d5ff" }),
    },
  ];

  return (
    <div>
      {/* Navigation Bar */}
      <NavBar />

      {/* Main Content */}
      <main style={{ padding: "20px" }}>
        {/* Heading and Date */}
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "20px",
          }}
        >
          <h1 style={{ fontFamily: "cursive", margin: 0 }}>
            Your Inbox At A Glance
          </h1>
          <p
            style={{
              fontFamily: "Arial, sans-serif",
              fontSize: "18px",
              margin: 0,
            }}
          >
            📅 {new Date().toLocaleDateString("en-GB", {
              day: "2-digit",
              month: "short",
              year: "numeric",
            })}
          </p>
        </div>

        {/* Category Columns */}
        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            justifyContent: "space-around",
            gap: "20px",
            marginTop: "100px",
          }}
        >
          {categories.map((category, index) => (
            <CategoryColumn
              key={index}
              title={category.title}
              cards={category.cards}
              bgColor={category.color}
            />
          ))}
        </div>
      </main>
    </div>
  );
};

export default App;
