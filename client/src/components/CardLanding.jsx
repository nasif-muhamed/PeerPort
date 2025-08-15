const Card = ({
    icon, 
    title,
    description,
    style = {}
}) => {
    return (
        <div className="card-primary animate-fade-in" style={style}>
            <div className="text-accent-primary text-4xl mb-4 flex justify-center"> {icon} </div>
            <h3 className="text-xl font-semibold mb-2"> {title} </h3>
            <p className="text-text-secondary"> {description} </p>
        </div>
    )
}

export default Card