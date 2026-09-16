import { parseJSONScript } from '../utils.js';
import { HeaderMain } from '../header.jsx';
import { ReleaseInfo } from '../info.jsx';
import { useState } from 'react';

function formSubmit (e) {
    e.preventDefault();

    const selectedDescriptors = Array.from(document.getElementsByClassName('selected'));
    const selectedDescriptorIdxs = selectedDescriptors.map(d => Number(d.dataset.descriptorIdx));

    const formData = new FormData(e.target);

    console.log(selectedDescriptorIdxs.length);

    const queryParams = new URLSearchParams({
        ...(formData.get('year') ? {'year': formData.get('year')} : {}),
        ...(selectedDescriptorIdxs.length !== 0 ? {'descriptors': JSON.stringify(selectedDescriptorIdxs)} : {})
    });

    const newURL = new URL(`${window.location.href.split('?')[0]}?${queryParams}`);
    window.location.href = newURL;
};

export default function App() {
    const top_5_data = parseJSONScript('top-5-data');
    const descriptors = [
        'Happy',
        'Sad',
        'Bittersweet',
        'Mellow',
        'Energetic',
        'Lighthearted',
        'Humorous',
        'Serious',
        'Surreal',
        'Sober',
        'Warm',
        'Cold',
        'Lush',
        'Harsh',
        'Bright',
        'Dark',
        'Soothing',
        'Anxious'
    ];

    const currentParams = new URLSearchParams(window.location.search);

    const [selectedDescriptors, setSelected] = (() => {
        const res = Array(descriptors.length).fill(false);
        if (currentParams.has('descriptors'))
            for (const d of JSON.parse(currentParams.get('descriptors'))) {
                res[Number(d)] = true;
            }

        return useState(res);
    })();

    const toggleDescriptor = (i) => {
        const newSelectedDescriptors = structuredClone(selectedDescriptors);
        newSelectedDescriptors[i] = !selectedDescriptors[i];

        setSelected(newSelectedDescriptors);
    }

    const [descriptorsOpen, setDescriptorsOpen] = useState(false);

    return <HeaderMain>
        <form onSubmit={formSubmit}>
            <label htmlFor="year">Year: </label>
            <input type="text" name="year" value={currentParams.get('year')}/>

            <br/><br/>

            <div>
                <div className="button" onClick={() => setDescriptorsOpen(!descriptorsOpen)}>Descriptors</div>
                {descriptorsOpen ? <div style={{height: '4em', overflowY: 'scroll'}}>
                    {Object.keys(descriptors).map(i => <><div className={selectedDescriptors[i] ? "button selected" : "button"} style={{
                        fontSize: '0.8em',
                        display: 'inline-block',
                        animation: 'fadeIn 0.2s ease-in-out'
                    }} data-descriptor-idx={i} onClick={() => toggleDescriptor(i)}>{descriptors[i]}</div>{i % 5 == 4 ? <br/> : <> </>}</>)}
                </div> : <div></div>}
            </div> <br/>

            <input type="submit" className="button"/>
        </form>

        <br></br>

        {top_5_data.map ((r, idx) =>
        <div>
            <span>{idx+1}</span>
            <ReleaseInfo release={r}/>
        </div>)}
    </HeaderMain>;
}
