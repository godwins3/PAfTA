'use client';
import { Button } from '@mui/material';
import { Link } from "../../components/Link/Link";
import styles from '../../styles/Nav.module.css';
import Userbutton from '../../components/UserButton/UserButton';

import { en } from '../../../translations';

interface HeaderProps {
    home: boolean;
}

export const Header = ({ home }: HeaderProps) => {
    const a = en;

    return (
        <div>
            <header className={styles.container}>
                <nav className={styles.nav}>
                    <a className={styles.nav__logo} href={"/"}>{a.logo}</a>
                    {home === true && (
                        <ul className={styles.nav__list}>
                            <li>
                                <Link href="/login">
                                    <Button className={styles.button} color="primary">{a.signin}</Button>
                                </Link>
                            </li>
                            <li>
                                <Link href="/register">
                                    <Button className={styles.button} color="primary">{a.signup}</Button>
                                </Link>
                            </li>
                        </ul>
                    )}
                    {home === false && (
                        <ul className={styles.nav__list}>
                            <li>
                                <Link href="/portifolio">
                                    <Button className={styles.button} color="primary">{a.wallet}</Button>
                                </Link>
                            </li>
                            <li>
                                <Link href="/trading">
                                    <Button className={styles.button} color="primary">{a.forextrade}</Button>
                                </Link>
                            </li>
                            <li>
                                <Link href="/transactions">
                                    <Button className={styles.button} color="primary">{a.transactions}</Button>
                                </Link>
                            </li>
                            <li>
                                <Link href="#">
                                    <Userbutton />
                                </Link>
                            </li>
                        </ul>
                    )}
                </nav>
            </header>
        </div>
    );
};

export default Header;
