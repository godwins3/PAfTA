import Header from "../components/Nav/Nav";
import styles from "../styles/Animation.module.css";

import { en } from '../../translations'; 


export default function Home() {
    const a = en;

    return (
        <main className={styles.mainBackground}>
            <Header home={false} />
            <div>
                <div className={styles.animated_title}>
                    <div className={styles.text_top}>
                        <div>
                            <span>{ a.phraseOne }</span>
                            <span>{ a.phraseTwo }</span>
                        </div>
                    </div>
                    <div className={styles.text_bottom}>
                        <div>{ a.phraseTree }</div>
                    </div>
                </div>
            </div>
        </main>
    )
}