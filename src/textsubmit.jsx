import { PostButton } from './post.jsx';
import { useState } from 'react';

export function TextSubmit() {
    const [text, setText] = useState('');

    return <div>
        <textarea onChange={e => setText(e.target.value)} style={{
            fontSize: '1.5em',
            minHeight: '2em',
            minWidth: '20vw',
            maxHeight: '25vh',
            maxWidth: '50vw',
            fieldSizing: 'content'
        }}/>
        <PostButton data={text}/>
    </div>;
}
