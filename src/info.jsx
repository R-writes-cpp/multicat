import { get_src_url } from './utils.js'

function Info({ page_path, img_path, children }) {
    return <div className="info">
        <div><a href={page_path}><img src={get_src_url(`/static${img_path}`)}></img></a></div>
        <div style={{flexDirection: 'column'}}>
            {children}
        </div>
    </div>;
}

export function UserInfo({ user }) {
    return <div>
        <Info page_path={`/users/${user.id}`} img_path={user.profile_picture}>
            <div><b>{user.username}</b></div>
            <div>Joined: {user.join_date}</div>
            <div>Location: {user.location}</div>
        </Info>

        <div className="button" onclick="follow" style={{fontSize: '1.5em'}}>Follow</div>
    </div>;
}

export function ReleaseInfo({ release, children }) {
    return <Info page_path={`/releases/${release.id}`} img_path={release.art}>
        <div><b>{release.title}</b></div>
        <div>{release.creator_primary.name}</div>
        <div>{release.release_date.slice(0, release.release_date.indexOf('-'))}</div>
        {children}
    </Info>;
}

export function ExtraReleaseInfo({ release, avg, ratingCount }) {
    const Media = Object.freeze({
        ALBUM: 0,
        BOOK: 1,
        FILM: 2
    });

    const creatorSecondaryLabel = (() => {
        switch (release.medium) {
            case Media.ALBUM:
                return 'Producer';

            case Media.BOOK:
                return 'Publisher';

            case Media.FILM:
                return 'Producer';
        }
    })();

    const lengthUnit = (() => {
        switch (release.medium) {
            case Media.ALBUM:
                return 'min';

            case Media.BOOK:
                return 'pg';

            case Media.FILM:
                return 'min';
        }
    })();

    return <ReleaseInfo release={release}>
        <div style={{fontSize: '0.75em'}}>
            <div>{creatorSecondaryLabel}: {release.creator_secondary.name}</div>
            <div>Length: {release.length} {lengthUnit}</div>
            <div>Language: {release.language}</div>
            <div><b>{avg}</b> from <b>{ratingCount}</b> {ratingCount == 1 ? 'user' : 'users'}</div>
        </div>
    </ReleaseInfo>;
}

export function ReleaseRatingInfo({ rating }) {
    return <ReleaseInfo release={rating.release}>
        <div>{rating.score}</div>
    </ReleaseInfo>;
}

export function RatingInfo({ rating }) {
    return <div className="info">
        <a href={`/users/${rating.user.id}`}><img src={get_src_url(`/static${rating.user.profile_picture}`)}></img></a>
        <span>{rating.user.username}: <b>{rating.score}</b></span>
    </div>
}
