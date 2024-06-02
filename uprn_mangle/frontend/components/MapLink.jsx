import "../css/maplink.css";

const MapLink = ({ Link, Icon, Lat, Lon }) => {
  return (
    <div>
      <a href={Link} target="_blank" rel="noopener noreferrer">
        <Icon />
      </a>
    </div>
  );
};

export default MapLink;
