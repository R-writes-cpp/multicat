import { useState } from 'react';
import { parseJSONScript } from './utils.js';

function HeaderButton({ clickFn, children }) {
    return <div onClick={clickFn}>
        {children}
    </div>;
}

function hamburgerMenu() {
    const logged_in = parseJSONScript('logged-in');

    return <div style={{
        textAlign: 'center',
        fontSize: '2em',
        fontWeight: 'bold',
        animation: 'fadeIn 0.2s ease-in-out',
        display: 'flex',
        flexDirection: 'column',
        flexGrow: '1'
    }}>
        <a className="button" href="/">Home</a>
        {
            logged_in ? <>
                <a className="button" href="/users">Profile</a>
                <a className="button" href="/rankings">Rankings</a>
                <a className="button" href="/recs">Recommendations</a>
                <a className="button" href="/logout">Log out</a>
            </> :
            <>
                <a className="button" href="/login">Log in</a>
                <a className="button" href="/signup">Sign up</a>
            </>
        }
    </div>
}

function searchMenu() {
    return <form action="/search" style={{
        display: 'flex',
        flexGrow: '1',
        justifyContent: 'center',
        animation: 'fadeIn 0.2s ease-in-out',
        alignItems: 'center',
        textAlign: 'center'
    }}>
        <div>
            <input type="text" name="q" style={{border: 'none', backgroundColor: '#dddddd'}}></input>
            <input className="button" type="submit" value="Submit"></input>
        </div>
    </form>
}

function Main({ states, children }) {
    function returnChildren() {
        return <div><div style={{animation: 'fadeIn 0.2s ease-in-out'}}>
            {children}
        </div></div>
    }

    return states.hamburger ? hamburgerMenu() :
        states.search ? searchMenu() : returnChildren();
}

export function HeaderMain({ children }) {
    const [hamburgerState, setHamburgerState] = useState(false);
    const [searchState, setSearchState] = useState(false);

    function hamburgerClick() {
        setHamburgerState(!hamburgerState);
        setSearchState(false); // no two states can be on at the same time
    }

    function searchClick() {
        setSearchState(!searchState);
        setHamburgerState(false); // ditto comment before
    }

    return <>
        <div id="header">
            <HeaderButton clickFn={() => {hamburgerClick();}}>☰</HeaderButton>
            <div>MultiCat</div>
            <HeaderButton clickFn={() => {searchClick();}}>⌕</HeaderButton>
        </div>
        <Main states={{hamburger: hamburgerState, search: searchState}}>
            {children}
        </Main>
    </>
}
