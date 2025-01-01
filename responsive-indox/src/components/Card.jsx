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
        width: '150px', // Fixed width
        height: '100px', // Fixed height
        display: 'flex', // Center text
        justifyContent: 'center', // Horizontally center
        alignItems: 'center', // Vertically center
        overflow: 'hidden', // Prevent overflow
        textOverflow: 'ellipsis', // Truncate long text
        whiteSpace: 'nowrap', // Prevent text wrapping
        boxShadow: '0 2px 5px rgba(0, 0, 0, 0.2)', // Optional: shadow for better look
      }}
    >
      {text}
    </div>
  );
};

export default Card;
