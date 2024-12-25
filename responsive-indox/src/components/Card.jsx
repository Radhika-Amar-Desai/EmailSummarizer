const Card = ({ text, bgColor }) => {
    return (
      <div
        style={{
          backgroundColor: bgColor,
          borderRadius: '8px',
          padding: '10px',
          margin: '10px',
          color: 'white',
          textAlign: 'center',
        }}
      >
        {text}
      </div>
    );
  };
  
  export default Card;
  