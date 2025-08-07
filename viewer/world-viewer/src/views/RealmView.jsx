import {useState} from 'react'

const realmData = {
    title: "hello realm!",
    imgSource: "./hello.jpg"
};

function MyButton({onClick}) {
    return (
        <button onClick={onClick}>Click Me</button>
    )
}

export function RealmView() {
    const [counter, setCounter] = useState(0);
    function handleClick() {
        setCounter(counter + 1)
    }
    return (
        <>
            <MyButton onClick={handleClick} />
            <h1>{realmData.title}</h1>
            <img src={realmData.imgSource} alt="realm image" />
            <p>narrative</p>
        </>
    )
}
