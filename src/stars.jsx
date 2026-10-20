import { useState } from 'react';
import { PostButton } from './post.jsx';
import Cookies from 'js-cookie';

export function StarStylesheet() {
    return <>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,100,0..1,0&icon_names=star_rate,star_rate_half" />
        <style>
            {`
                .material-symbols-outlined {
                    font-size: 2.5em;
                }
            `}
        </style>
    </>;
}

function EmptyStar() {
    return <span className="material-symbols-outlined">star_rate</span>;
}

function HalfStar() {
    return <span className="material-symbols-outlined">star_rate_half</span>;
}

function FullStar() {
    return <span className="material-symbols-outlined" style={{fontVariationSettings: "'FILL' 1"}}>star_rate</span>;
}

function ScoreStar({ currentScore, setState, star }) {
    const starDisplay = (() => {
        if (currentScore + 1 == star)
            return <HalfStar/>;
        else
            return (currentScore < star) ? <EmptyStar/> : <FullStar/>;
    })();

    return <span onClick={e => {
        const clickedStar = e.currentTarget;
        const isHalfStar = e.nativeEvent.offsetX < clickedStar.offsetWidth / 2;

        setState(star - (isHalfStar ? 1 : 0));
    }}>
        {starDisplay}
    </span>
}

export function RatingField({ currentRating }) {
    const [rating, setRating] = useState(currentRating);
    const starRatings = [2, 4, 6, 8, 10]

    return <>
        {starRatings.map(i =>
            <ScoreStar currentScore={rating} setState={setRating} star={i}/>
        )}

        <PostButton data={rating} path={'/rate'}/>
    </>;
}

const Descriptor = Object.freeze({
    0: 'Happy',
    1: 'Sad',
    2: 'Bittersweet',
    3: 'Mellow',
    4: 'Energetic',
    5: 'Lighthearted',
    6: 'Humorous',
    7: 'Serious',
    8: 'Surreal',
    9: 'Sober',
    10: 'Warm',
    11: 'Cold',
    12: 'Lush',
    13: 'Harsh',
    14: 'Bright',
    15: 'Dark',
    16: 'Soothing',
    17: 'Anxious'
});

export function VotingField({ currentScore, descriptorIdx, setScore }) {
    const descriptorName = Descriptor[descriptorIdx];
    const starScores = [2, 4];

    return <div>
        <span>{descriptorName}</span>
        {starScores.map(i =>
            <ScoreStar currentScore={currentScore} setState={(score) => setScore(descriptorIdx, score)} star={i}/>
        )}
    </div>;
}

export function VotingFieldGroup({ currentScores }) {
    const [scores, setScores] = useState(currentScores);
    const setScore = (idx, score) => {
        const newScores = structuredClone(scores);
        newScores[idx] = score;
        setScores(newScores);
    };

    return <>
        {scores.map((score, idx) => <VotingField currentScore={score} descriptorIdx={idx} setScore={(idx, score) => setScore(idx, score)}/>)}
        <PostButton data={scores}/>
    </>;
}
