import React, { useState } from "react";
import { LuSmilePlus } from "react-icons/lu";
import NavBar from "./components/NavBar";
import CategoryColumn from "./components/CategoryColumn";
import DefineCustomCategory from "./components/DefineCustomCategory";

const App = () => {
  const [categories, setCategories] = useState([
    {
      title: "Category-one",
      color: "#F5EFFF",
      titleBoxColor: "#E0C3FC",
      cards: Array(5).fill({ text: "wertrcyvu byi", color: "#D7B8F8" }),
    },
    {
      title: "Category-two",
      color: "#F3FBEA",
      titleBoxColor: "#B7E5D3",
      cards: Array(4).fill({ text: "wertrcyvu byi", color: "#6FDB83" }),
    },
    {
      title: "Category-three",
      color: "#E3F5FA",
      titleBoxColor: "#A4D9EC",
      cards: Array(5).fill({ text: "wertrcyvu byi", color: "#7BD3EA" }),
    },
  ]);

  const [isModalOpen, setIsModalOpen] = useState(false);

  const addCategory = (titles) => {
    const newCategories = titles.map((title) => ({
      title,
      color: "#FFF6E5",
      titleBoxColor: "#FFD27D",
      cards: [],
    }));
    setCategories((prev) => [...prev, ...newCategories]);
  };

  return (
    <div>
      <NavBar />
      <main style={{ padding: "20px" }}>
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "20px",
          }}
        >
          <h1
            style={{
              fontFamily: "cursive",
              margin: 0,
              fontSize: "32px",
              marginLeft: "162px",
              marginTop: "64px",
              fontWeight: 400,
            }}
          >
            Your Inbox At A Glance
          </h1>
          <p
            style={{
              fontFamily: "Arial, sans-serif",
              fontSize: "15px",
              margin: 0,
              marginTop: "67px",
              marginLeft: "690px",
            }}
          >
            📅 {new Date().toLocaleDateString("en-GB", {
              day: "2-digit",
              month: "short",
              year: "numeric",
            })}
          </p>
        </div>

        <div
          style={{
            display: "flex",
            justifyContent: "flex-end",
            alignItems: "center",
            marginBottom: "30px",
            fontFamily: "cursive",
            fontSize: "20px",
            color: "#5A5A5A",
            cursor: "pointer",
          }}
          onClick={() => setIsModalOpen(true)}
        >
          <LuSmilePlus style={{ marginRight: "8px" }} />
          Define Custom Categories
        </div>

        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            justifyContent: "space-around",
            gap: "20px",
            marginTop: "50px",
          }}
        >
          {categories.map((category, index) => (
            <CategoryColumn
              key={index}
              title={category.title}
              cards={category.cards}
              bgColor={category.color}
              titleBoxColor={category.titleBoxColor}
            />
          ))}
        </div>

        {isModalOpen && (
          <DefineCustomCategory
            onAddCategory={addCategory}
            onClose={() => setIsModalOpen(false)}
          />
        )}
      </main>
    </div>
  );
};

export default App;
