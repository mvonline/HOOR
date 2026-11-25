import React, { useEffect, useMemo, useState } from 'react';
import { marked } from 'marked';
import TangoPage, { CLIPS } from './Tango';
import { unlock, lock, mediaUrl as media, mapUrl } from './transport';
import {
  BookOpen,
  Map as MapIcon,
  MapPin,
  Search,
  Users,
  Images,
  Menu,
  X,
  LogOut,
  ChevronLeft,
  ChevronRight,
  LockKeyhole,
  Eye,
  EyeOff,
  Sun,
  Moon,
  Compass,
  Shield,
  Printer,
  Check,
  AlertCircle,
  MessageSquare,
  CarFront,
  Clapperboard,
  ScrollText,
  Music2,
  Play,
} from 'lucide-react';

type Doc = {
  id: string;
  file: string;
  title: string;
  category: string;
  description: string;
  markdown: string;
  legacy: boolean;
  spoiler: boolean;
  words: number;
};
type Picture = {
  id: string;
  title: string;
  filename: string;
  category: string;
  caption: string;
  retired: boolean;
};
type SourceLink = { docId: string; section: string };
type DialogueScene = {
  id: string;
  title: string;
  context: string;
  lines: { speaker: string; text: string }[];
  source: SourceLink;
};
type DialogueRecording = {
  id: string;
  title: string;
  context: string;
  markdown: string;
  source: SourceLink;
};
type EditionKey = 'v13' | 'v12' | 'v11';
type EditionBundle = {
  docs: Doc[];
  budget: any;
  chapters: { number: number; title: string; minutes: number }[];
  sideStories: { id: string; title: string; markdown: string }[];
  people: {
    name: string;
    age: number;
    role: string;
    image: string | null;
    text: string;
    quote?: string;
  }[];
  chapterSummaries: string[];
  copy: {
    heroTitle: string;
    heroText: string;
    storyLead: string;
    mapLead: string;
    mapTitles: string[];
    mapTexts: string[];
  };
  dialogues?: {
    chapters: { number: number; title: string; scenes: DialogueScene[] }[];
    recordings: DialogueRecording[];
    note: string;
  };
};
type Library = EditionBundle & {
  readerEdition?: Record<string, { title: string; markdown: string }>;
  gallery: Picture[];
  editions?: Partial<Record<EditionKey, EditionBundle>>;
};

const fa = (n: number) => n.toLocaleString('fa-IR');
const release = { major: 1, minor: 7, patch: 0, build: '20261125.1' };
const normalize = (s: string) =>
  s
    .replace(/ي/g, 'ی')
    .replace(/ك/g, 'ک')
    .replace(/[\u200c\u064b-\u065f]/g, '')
    .toLowerCase();

const labels = [
  ['home', 'معرفی پروژه', BookOpen],
  ['tango', 'ویدیوهای واقعیِ منطقه', Clapperboard],
  ['overview', 'ایده و داستان کلی', ScrollText],
  ['read', 'فیلم‌نامه', BookOpen],
  ['novel', 'رمان', BookOpen],
  ['dialogues', 'گفت‌وگوها', MessageSquare],
  ['places', 'محل‌ها', MapPin],
  ['story', 'آدم‌ها', Users],
  ['vehicles', 'وسیله‌ها', CarFront],
  ['gallery', 'گالری رسانه‌ها', Images],
  ['maps', 'نقشه', MapIcon],
  ['missions', 'فصل‌ها و مأموریت‌ها', Compass],
  ['direction', 'اصول کارگردانی', Eye],
  ['library', 'اسناد طراحی', Shield],
] as const;

const navGroups = [
  ['معرفی و ویدیوهای واقعی', ['home', 'tango']],
  ['داستان و روایت', ['overview', 'read', 'novel', 'dialogues']],
  ['جهان بازی', ['places', 'story', 'vehicles', 'gallery', 'maps']],
  ['طراحی و تولید', ['missions', 'direction', 'library']],
] as const;

const introUrl = (f: string) => new URL('./media/intro/' + f, document.baseURI).pathname;
const galleryMediaUrl = (f: string) => new URL('./media/gallery/' + f, document.baseURI).pathname;

const generatedVideos = [
  { title: 'ویدیوی مفهومی ۱', file: 'generated-scene-01.mp4', note: 'ویدیوی تولیدشدهٔ پروژه · ۲۲ نوامبر ۲۰۲۶' },
  { title: 'ویدیوی مفهومی ۲', file: 'generated-scene-02.mp4', note: 'ویدیوی تولیدشدهٔ پروژه · ۲۲ نوامبر ۲۰۲۶' },
  { title: 'ویدیوی مفهومی ۳', file: 'generated-scene-03.mp4', note: 'ویدیوی تولیدشدهٔ پروژه · ۲۲ نوامبر ۲۰۲۶' },
  { title: 'ویدیوی مفهومی ۴', file: 'generated-scene-04.mp4', note: 'ویدیوی تولیدشدهٔ پروژه · ۲۲ نوامبر ۲۰۲۶' },
  { title: 'ویدیوی مفهومی ۵', file: 'generated-scene-05.mp4', note: 'ویدیوی تولیدشدهٔ پروژه · ۲۲ نوامبر ۲۰۲۶' },
];

const musicTracks = [
  { title: 'Desert Dawn', subtitle: 'سپیده‌دمِ کویر', file: 'desert-dawn.mp3' },
  { title: 'Three-Note Motif', subtitle: 'نقش‌مایهٔ سه‌نتی', file: 'three-note-motif.mp3' },
  { title: 'سه نوته راز', subtitle: 'موتیفِ راز', file: 'three-note-secret.mp3' },
  { title: 'سفر کویر', subtitle: 'موسیقیِ سفر', file: 'desert-journey.mp3' },
];

const chapterImages = [
  'env-l03-logistics-yard-v1',
  'env-l05-kalut-markers-v1',
  'daniyal-camel-riding-v2',
  'v11-action-kalut-convoy-v1',
  'daniyal-drone-v2',
  'env-c03-erosion-tunnel-v1',
  'caravanserai-night-v1',
  'daniyal-quad-atv-v2',
  'caravanserai-night-v1',
  'env-c06-r17-field-ledge-v1',
  'env-c02-expedition-camp-v1',
  'env-c08-collapse-routes-v1',
  'daniyal-motorcycle-v2',
  'env-c07-core-perimeter-v1',
  'canyon-day-v1',
];

function sceneize(html: string) {
  return html
    .replace(
      /<h3 id="(section-\d+)">نما\s*([\d۰-۹]+ب?)\s*—\s*([^<]+?)<\/h3>/g,
      (_, id, n, t) => `<h3 id="${id}" class="scene"><span>نما ${n}</span>${t.replace(/\s*\[[^\]]+\]\s*$/, '')}</h3>`,
    )
    .replace(/<p><strong>(M\d\d)،\s*([^<]+?):<\/strong>\s*/g, (_, id, t) => `<h3 class="scene"><span>${id}</span>${t}</h3><p>`)
    .replace(
      /<p><strong>نما\s*([\d۰-۹]+ب?)\s*—\s*([^<]+?)<\/strong><\/p>/g,
      (_, n, t) => `<h3 class="scene"><span>نما ${n}</span>${t.replace(/\s*\[[^\]]+\]\s*$/, '')}</h3>`,
    )
    .replace(
      /<p><strong>(شبِ کمپ)،\s*فصل\s*[^<]+?:<\/strong>\s*/g,
      (_, t) => `<h3 class="scene camp"><span>کمپ</span>${t}</h3><p>`,
    );
}

function dialogueize(html: string) {
  const line = /^([^:\n]{1,180}?):\s*«([\s\S]+)»\s*$/;
  return html.replace(/<p>([\s\S]*?)<\/p>/g, (whole: string, body: string) => {
    const parts = body.split(/<br\s*\/?>\s*/);
    if (!parts.some((p) => line.test(p.replace(/<[^>]+>/g, '').trim()))) return whole;
    let out = '';
    let open = false;
    for (const p of parts) {
      const plain = p.replace(/<[^>]+>/g, '').trim();
      const m = plain.match(line);
      if (m) {
        if (!open) {
          out += '<div class="dlg">';
          open = true;
        }
        out += `<p><b>${m[1]}</b><span>${m[2]}</span></p>`;
      } else {
        if (open) {
          out += '</div>';
          open = false;
        }
        if (plain) out += `<p>${p}</p>`;
      }
    }
    return out + (open ? '</div>' : '');
  });
}

function storyChapters(md: string) {
  const body = md;
  const parts = body.split(/\n(?=## )/).map((p) => p.replace(/\n---\s*$/, ''));
  const pro = parts.find((p) => p.startsWith('## پیش‌درآمد'));
  const epi = parts.find((p) => p.startsWith('## اپیلوگ'));
  const chs = parts.filter((p) => /^## فصل [\d۰-۹]+ —/.test(p));
  if (pro && chs.length) {
    const [h, ...r] = chs[0].split('\n');
    const [proHeadRaw, ...proRest] = pro.split('\n');
    const proHead = proHeadRaw.replace(/^##\s*/, '### ');
    const ch1SubHead = '### ' + h.replace(/^##\s*/, '');
    chs[0] =
      h +
      '\n\n' +
      proHead +
      '\n\n' +
      proRest.join('\n').trim() +
      '\n\n---\n\n' +
      ch1SubHead +
      '\n\n' +
      r.join('\n').trim();
  }
  if (epi && chs.length) {
    chs[chs.length - 1] = chs[chs.length - 1] + '\n\n---\n\n' + epi;
  }
  return { chapters: chs, cast: parts.find((p) => p.startsWith('## آدم‌های کمپ')) || '' };
}

type NovelChapter = { title: string; part: string; date: string; markdown: string; words: number };
function parseNovel(md: string): NovelChapter[] {
  const lines = md.split('\n');
  const chapters: NovelChapter[] = [];
  let part = 'رمان';
  let current: { title: string; part: string; lines: string[] } | null = null;
  const save = () => {
    if (current) {
      const date = current.lines[0]?.match(/^\*\((.+)\)\*$/)?.[1] || '';
      const markdown = current.lines.join('\n').replace(/^\*\([^\n]*\)\*\s*\n?/, '').trim();
      chapters.push({ ...current, date, markdown, words: markdown.split(/\s+/).filter(Boolean).length });
    }
  };
  for (const line of lines) {
    if (line.startsWith('# بخش')) {
      part = line.replace(/^#\s*/, '').trim();
      continue;
    }
    if (/^## (فصل [۰-۹0-9]+ —|اپیلوگ —)/.test(line)) {
      save();
      current = { title: line.replace(/^##\s*/, '').trim(), part, lines: [] };
      continue;
    }
    if (current) current.lines.push(line);
  }
  save();
  return chapters;
}

function documentHref(id: string, mode: 'read' | 'full' = 'full', section = '') {
  const target = new URL(mode === 'full' ? './viewer.html' : './', document.baseURI);
  target.searchParams.set('doc', id);
  target.searchParams.set('mode', mode);
  if (section) target.searchParams.set('section', section);
  return target.pathname + target.search;
}

function markdownHTML(markdown: string, breaks = false, story = false) {
  const renderer = new marked.Renderer();
  renderer.html = ({ text }: any) =>
    /^<br\s*\/?>(?:\n)?$/i.test(text) ? '<br>' : text.replace(/</g, '&lt;').replace(/>/g, '&gt;');
  renderer.link = ({ href, text }: any) => {
    if (!href || /^(javascript|data):/i.test(href)) return text;
    return `<a href="${href.replace(/"/g, '&quot;')}" ${/^https?:/.test(href) ? 'target="_blank" rel="noopener noreferrer"' : ''}>${text}</a>`;
  };
  renderer.image = ({ href, text }: any) => {
    const filename = href?.split('/').pop()?.replace(/\.png$/, '');
    return filename && /^(region-map|canyon-map|design-map)$/.test(filename)
      ? `<img src="${media(filename)}" alt="${text || 'نقشه'}" loading="lazy"/>`
      : `<span class="image-note">${text || 'مرجع تصویری در گالری'}</span>`;
  };
  renderer.code = ({ text, lang }: any) =>
    lang === 'mermaid'
      ? `<figure><img src="${media('design-map')}" alt="نمودار اتصال مناطق"/><figcaption>شماتیک اتصال مناطق؛ نقشهٔ جغرافیایی نیست.</figcaption></figure>`
      : `<pre dir="auto">${text.replace(/&/g, '&amp;').replace(/</g, '&lt;')}</pre>`;
  const screenplay = story
    ? markdown
        .replace(/^\*\*(نما\s*[\d۰-۹]+ب?\s*—\s*[^\n]+)\*\*\s*$/gm, '### $1')
        .replace(/^\*\[([^\n]+)\]\*\s*$/gm, '*$1*')
    : markdown;
  let i = 0;
  const out = (marked.parse(screenplay, { renderer, gfm: true, breaks }) as string).replace(
    /<h([1234])>/g,
    (_, n) => `<h${n} id="section-${i++}">`,
  );
  return story ? dialogueize(sceneize(out)) : out;
}

function RichText({
  text,
  onNavigate,
  breaks = false,
  story = false,
}: {
  text: string;
  onNavigate?: (file: string) => void;
  breaks?: boolean;
  story?: boolean;
}) {
  const html = useMemo(() => markdownHTML(text, breaks, story), [text, breaks, story]);
  return (
    <div
      className={story ? 'prose reader-prose' : 'prose'}
      onClick={(e) => {
        const a = (e.target as HTMLElement).closest('a');
        if (a) {
          const href = a.getAttribute('href') || '';
          if (href && !/^(https?:|mailto:|#)/.test(href)) {
            e.preventDefault();
            onNavigate?.(href.split('/').pop()!.split('#')[0]);
          }
        }
      }}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}

export default function Page() {
  const [library, setLibrary] = useState<Library | null>(null);
  const [edition, setEdition] = useState<EditionKey | null>(null);
  const [loading, setLoading] = useState(false);
  const [authenticated, setAuthenticated] = useState(false);
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const [busyText, setBusyText] = useState('در حال باز کردن…');
  const [tab, setTab] = useState('home');
  const [docId, setDocId] = useState<string | null>(null);
  const [menu, setMenu] = useState(false);
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('همه');
  const [galleryMediaMode, setGalleryMediaMode] = useState('images');
  const [chapter, setChapter] = useState(1);
  const [missionMode, setMissionMode] = useState('main');
  const [overviewPage, setOverviewPage] = useState(1);
  const [map, setMap] = useState('region-map');
  const [lightbox, setLightbox] = useState<string | null>(null);
  const [spoilers, setSpoilers] = useState<Record<string, boolean>>({});
  const [dark, setDark] = useState(false);
  const [reviewCopied, setReviewCopied] = useState(false);
  const [sectionTarget, setSectionTarget] = useState('');
  const [viewMode, setViewMode] = useState<'read' | 'full'>('read');
  const [dialogueChapter, setDialogueChapter] = useState(1);
  const [dialogueMode, setDialogueMode] = useState('scenes');
  const [readIdx, setReadIdx] = useState(0);
  const [readOk, setReadOk] = useState(false);
  const [novelIdx, setNovelIdx] = useState(0);
  const [novelOk, setNovelOk] = useState(false);

  const activeLib = useMemo<Library | null>(() => {
    if (!library) return null;
    const key: EditionKey = edition || 'v13';
    const ed = library.editions?.[key];
    if (!ed) return library;
    return {
      ...ed,
      gallery: library.gallery,
      readerEdition: key === 'v11' ? library.readerEdition : undefined,
      dialogues: key === 'v11' ? library.dialogues : ed.dialogues || library.dialogues,
      editions: library.editions,
    };
  }, [library, edition]);

  const isV13 = edition === 'v13';
  const isV12 = edition === 'v12';
  const isModern = isV13 || isV12;
  const editionLabel = isV13 ? 'نسخهٔ ۱۳' : isV12 ? 'نسخهٔ ۱۲' : 'نسخهٔ ۱۱';
  const editionTag = isV13
    ? 'نسخهٔ ۱۳ (سنتزِ نهاییِ کانن)'
    : isV12
      ? 'نسخهٔ ۱۲ (اکشنِ بین‌المللی — آرشیو)'
      : 'نسخهٔ ۱۱ (روایتِ درامِ بومی — آرشیو)';
  const screenplayDocId = isV13
    ? 'SCREENPLAY_V13_FA'
    : isV12
      ? 'SCREENPLAY_V12_FA'
      : 'SCREENPLAY_V11_FA';
  const novelDocId = isV13
    ? 'RAD_E_HOOR_NOVEL_V13_FA'
    : isV12
      ? 'RAD_E_HOOR_NOVEL_V12_FA'
      : 'RAD_E_HOOR_NOVEL_FA';

  useEffect(() => {
    function key(e: KeyboardEvent) {
      if (e.key === 'Escape') {
        setLightbox(null);
        setMenu(false);
      }
      if (lightbox && activeLib && ['ArrowLeft', 'ArrowRight'].includes(e.key)) {
        const list = activeLib.gallery;
        const i = list.findIndex((x) => x.id === lightbox);
        if (i >= 0) setLightbox(list[(i + (e.key === 'ArrowLeft' ? 1 : -1) + list.length) % list.length].id);
      }
    }
    window.addEventListener('keydown', key);
    document.body.style.overflow = lightbox ? 'hidden' : '';
    return () => {
      window.removeEventListener('keydown', key);
      document.body.style.overflow = '';
    };
  }, [lightbox, activeLib]);

  useEffect(() => {
    const readRoute = () => {
      const params = new URLSearchParams(location.search);
      const legacy = location.hash.startsWith('#doc=') ? decodeURIComponent(location.hash.slice(5)) : null;
      const id = params.get('doc') || legacy;
      if (id) {
        setDocId(id);
        setViewMode(
          params.get('mode') === 'read'
            ? 'read'
            : location.pathname.endsWith('/viewer.html') || params.get('mode') === 'full'
              ? 'full'
              : 'read',
        );
        setSectionTarget(params.get('section') || '');
        setTab('library');
      }
    };
    readRoute();
    window.addEventListener('popstate', readRoute);
    return () => window.removeEventListener('popstate', readRoute);
  }, [authenticated]);

  useEffect(() => {
    if (sectionTarget) {
      const found = [...document.querySelectorAll('.prose h2,.prose h3')].find((h) =>
        normalize(h.textContent || '').includes(normalize(sectionTarget)),
      );
      if (found) {
        found.scrollIntoView();
        setSectionTarget('');
      }
    }
  }, [docId, sectionTarget, spoilers, authenticated, viewMode, activeLib]);

  function navigate(next: string) {
    setTab(next);
    setDocId(null);
    setMenu(false);
    setCategory('همه');
    setQuery('');
    history.replaceState(null, '', new URL('./', document.baseURI).pathname);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function switchEdition(next: EditionKey) {
    setEdition(next);
    setDocId(null);
    setReadIdx(0);
    setNovelIdx(0);
    setDialogueChapter(1);
    setDialogueMode('scenes');
    setChapter(1);
    setCategory('همه');
    setQuery('');
    setMenu(false);
    setReviewCopied(false);
    history.replaceState(null, '', new URL('./', document.baseURI).pathname);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function openDoc(id: string, section = '', mode: 'read' | 'full' = 'read') {
    const selectedMode = section ? 'full' : mode;
    setDocId(id);
    setViewMode(selectedMode);
    setMenu(false);
    setQuery('');
    setSectionTarget(section);
    history.replaceState(null, '', documentHref(id, selectedMode, section));
    window.scrollTo({ top: 0 });
  }

  function openFile(file: string) {
    if (file === 'map.html') {
      window.open(mapUrl(), '_blank', 'noopener,noreferrer');
      return;
    }
    if (file === 'README.md') {
      openDoc('READER_GUIDE_FA');
      return;
    }
    const d = activeLib?.docs.find((x) => x.file.split('/').pop() === decodeURIComponent(file));
    if (d) openDoc(d.id);
    else if (/\.(html|json)$/.test(file)) navigate(file.includes('map') ? 'maps' : 'missions');
    else if (/\.(png|svg)$/.test(file)) setLightbox(file.replace(/\.(png|svg)$/, ''));
  }

  async function login(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError('');
    setBusyText('در حال دریافت کتاب…');
    try {
      const contents = await unlock(password, setBusyText);
      setLibrary(contents as Library);
      setEdition(null);
      setAuthenticated(true);
      setPassword('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'باز کردن کتاب ممکن نشد. دوباره تلاش کنید.');
    } finally {
      setBusy(false);
      setLoading(false);
    }
  }

  function logout() {
    lock();
    setLibrary(null);
    setEdition(null);
    setAuthenticated(false);
    setDocId(null);
    setTab('home');
    setLightbox(null);
    setQuery('');
    setSpoilers({});
    setReviewCopied(false);
    setViewMode('read');
    history.replaceState(null, '', new URL('./', document.baseURI).pathname);
  }

  const doc = activeLib?.docs.find((x) => x.id === docId);
  const readerEdition = doc ? activeLib?.readerEdition?.[doc.id] : undefined;
  const summaryActive = !!readerEdition && viewMode === 'read';
  const activeMarkdown = doc ? (summaryActive ? readerEdition!.markdown : doc.markdown) : '';
  const activeTitle = summaryActive ? readerEdition!.title : doc?.title;

  useEffect(() => {
    document.title =
      authenticated && edition && activeTitle
        ? activeTitle + ' | ردِ هور'
        : authenticated && edition
          ? `ردِ هور (${editionLabel}) | داستان و راهنمای بازی`
          : 'ردِ هور | داستان و راهنمای بازی';
  }, [authenticated, edition, activeTitle, editionLabel]);

  const dialogue = activeLib?.dialogues?.chapters.find((c) => c.number === dialogueChapter);
  const hasRecordings = (activeLib?.dialogues?.recordings?.length || 0) > 0;

  const searchResults = useMemo(() => {
    if (!activeLib || query.trim().length < 2) return [];
    const q = normalize(query.trim());
    return activeLib.docs.flatMap((d) => {
      const plain = activeLib.readerEdition?.[d.id];
      const plainIndex = plain ? normalize(plain.title + ' ' + plain.markdown).indexOf(q) : -1;
      const fullIndex = normalize(d.title + ' ' + d.markdown).indexOf(q);
      if (plainIndex < 0 && fullIndex < 0) return [];
      const usePlain = !!plain && plainIndex >= 0;
      const text = usePlain ? plain!.markdown : d.markdown;
      const index = normalize(text).indexOf(q);
      const start = Math.max(0, index - 70);
      return [
        {
          ...d,
          title: usePlain ? plain!.title : d.title,
          snippet: text.slice(start, start + 220).replace(/[#*|]/g, ''),
          resultMode: (usePlain ? 'read' : 'full') as 'read' | 'full',
          sourceLabel: usePlain ? 'توضیح ساده' : 'متن کامل',
        },
      ];
    });
  }, [query, activeLib]);

  const toc = doc
    ? [...activeMarkdown.matchAll(/^(#{1,4}) (.+)$/gm)].map((m, i) => ({
        level: m[1].length,
        title: m[2].replace(/[*`]/g, ''),
        id: 'section-' + i,
      }))
    : [];

  const pic = activeLib?.gallery.find((x) => x.id === lightbox);

  const story = useMemo(() => {
    const d =
      activeLib?.docs.find((x) => x.id === 'SCREENPLAY_V13_FA') ||
      activeLib?.docs.find((x) => x.id === 'SCREENPLAY_V12_FA') ||
      activeLib?.docs.find((x) => x.id === 'SCREENPLAY_V11_FA') ||
      activeLib?.docs.find((x) => x.id === 'SCREENPLAY_FILM_FA');
    return d ? storyChapters(d.markdown) : null;
  }, [activeLib]);

  const novel = useMemo(() => {
    const d =
      activeLib?.docs.find((x) => x.id === 'RAD_E_HOOR_NOVEL_V13_FA') ||
      activeLib?.docs.find((x) => x.id === 'RAD_E_HOOR_NOVEL_V12_FA') ||
      activeLib?.docs.find((x) => x.id === 'RAD_E_HOOR_NOVEL_FA');
    return d ? parseNovel(d.markdown) : null;
  }, [activeLib]);

  const heroImg = activeLib?.gallery.some((g) => g.id === 'v11-action-kalut-convoy-v1')
    ? 'v11-action-kalut-convoy-v1'
    : 'canyon-day-v1';

  const galleryVideos = [
    { title: 'پیش‌درآمدِ ردِ هور', note: 'ویدیوی معرفیِ پروژه', src: introUrl('rad-e-hoor-intro.mp4') },
    ...CLIPS.map((c) => ({
      title: c.title,
      note: 'فیلم‌برداریِ واقعیِ منطقهٔ تنگه و لوت · ' + c.mins,
      src: new URL('./media/tango/' + c.n + '.mp4', document.baseURI).pathname,
    })),
    ...generatedVideos.map((v) => ({ title: v.title, note: v.note, src: galleryMediaUrl(v.file) })),
  ];

  if (loading)
    return (
      <main className="login-page">
        <div className="loading">
          <span className="sun-mark">☀</span>
          <p>در حال باز کردن کتاب طراحی…</p>
        </div>
      </main>
    );

  if (!authenticated || !library)
    return (
      <main className="login-page">
        <div className="login-orbit" />
        <div className="login-card">
          <span className="eyebrow">RAD-E HOOR · DESIGN BIBLE</span>
          <div className="brand-title">
            ردِ هور<span>داستان، رمان و کتابِ طراحی بازی</span>
          </div>
          <p>
            اکشنِ نیمه‌بازِ کویرِ لوت و رازِ تنگهٔ هور.
            <br />
            برای ورود، رمز دریافتی را وارد کنید.
          </p>
          <form onSubmit={login}>
            <label htmlFor="password">رمز ورود</label>
            <div className="password-field">
              <LockKeyhole size={18} />
              <input
                id="password"
                type={showPassword ? 'text' : 'password'}
                autoComplete="current-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                dir="ltr"
                aria-describedby={error ? 'login-error' : undefined}
              />
              <button
                type="button"
                className="icon-button"
                aria-label={showPassword ? 'پنهان کردن رمز' : 'نمایش رمز'}
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
            {error && (
              <p className="error" id="login-error" role="alert">
                {error}
              </p>
            )}
            <button className="primary" disabled={busy}>
              {busy ? busyText : 'ورود به کتاب طراحی'}
            </button>
          </form>
          <small>ردِ هور · نسخهٔ ۱۳ (سنتزِ نهایی) · نسخهٔ ۱۲ و نسخهٔ ۱۱ (آرشیو)</small>
        </div>
      </main>
    );

  // Upfront Version Picker Screen immediately after login
  if (!edition)
    return (
      <main className="login-page picker-page">
        <div className="login-orbit" />
        <section className="edition-picker" aria-labelledby="picker-title">
          <header className="picker-header">
            <span className="eyebrow">RAD-E HOOR · انتخاب نسخه</span>
            <h1 id="picker-title">کدام نسخه از ردِ هور را می‌خواهید بخوانید؟</h1>
            <p>
              هر سه نسخه به‌صورت کامل در این پرتال در دسترس‌اند و هر زمان در نوارِ کناری می‌توانید میانِ آن‌ها جابه‌جا شوید.
            </p>
          </header>
          <div className="edition-cards">
            <article className="edition-card featured" onClick={() => switchEdition('v13')}>
              <div className="edition-card-top">
                <span className="edition-badge canon">جدید · Canon فعلی</span>
                <span className="edition-code" dir="ltr">
                  v13
                </span>
              </div>
              <h2>نسخهٔ ۱۳ — سنتزِ نهایی</h2>
              <p>
                تلفیقِ نهاییِ ستونِ اخلاقیِ «نام و گناه» (تصادفِ سام و همدستیِ دانیال، افشای یگانه در فصل ۱۰) با ساعتِ
                شنیِ ۶روزهٔ پروازِ ویکتور کروز: ۲ قلهٔ وحشتِ Mk-1 با مکانیکِ فریادزدنِ اسم، سرپیچیِ ۴۰۰هزار دلاریِ سارا،
                لاگرِ پویا، مهارِ قابل‌بازیِ هواپیما با وینچِ ۱۰تُنی و اپیلوگِ درِ چوبیِ شهداد.
              </p>
              <div className="edition-meta">
                <span>۱۵ فصل + پیش‌درآمد و اپیلوگ</span>
                <span>۴۱ مأموریت اصلی (M00–M40)</span>
                <span>رمانِ کامل v13</span>
                <span>۱۷ شخصیت</span>
              </div>
              <button
                type="button"
                className="primary"
                onClick={(e) => {
                  e.stopPropagation();
                  switchEdition('v13');
                }}
              >
                ورود به نسخهٔ ۱۳
              </button>
            </article>

            <article className="edition-card" onClick={() => switchEdition('v12')}>
              <div className="edition-card-top">
                <span className="edition-badge archive">آرشیو</span>
                <span className="edition-code" dir="ltr">
                  v12
                </span>
              </div>
              <h2>نسخهٔ ۱۲ — اکشنِ بین‌المللی</h2>
              <p>
                اکشن-تریلر بین‌المللی (MGSV + Mad Max + Sicario + RE4)، ۴۸ ساعتِ پاک‌شدهٔ دانیال، سلاحِ زیستیِ H-0 برای
                PMCها، پویا دلالِ دیوانهٔ بازارِ سیاه، باندِ پروازِ نمکزار و پایانِ سردِ «سایت ۰۱» — بدونِ ملودرام، درامِ
                خانوادگی یا سیاست.
              </p>
              <div className="edition-meta">
                <span>۱۵ فصل فیلم‌نامه</span>
                <span>رمانِ کامل v12</span>
                <span>۱۷ شخصیت</span>
                <span>۲۳ مأموریت فرعی</span>
              </div>
              <button
                type="button"
                className="edition-secondary-btn"
                onClick={(e) => {
                  e.stopPropagation();
                  switchEdition('v12');
                }}
              >
                ورود به نسخهٔ ۱۲
              </button>
            </article>

            <article className="edition-card" onClick={() => switchEdition('v11')}>
              <div className="edition-card-top">
                <span className="edition-badge archive">آرشیو</span>
                <span className="edition-code" dir="ltr">
                  v11
                </span>
              </div>
              <h2>نسخهٔ ۱۱ — روایتِ درامِ بومی</h2>
              <p>
                روایتِ دراماتیکِ کویرِ لوت با خطِ داستانیِ سام، کاروانسرای رویا، پویا تورلیدرِ سافاری و اپیلوگِ شهداد (به
                همراه رمانِ ۲۶۵ صفحه‌ای، خلاصه‌های ساده و آرشیوِ پیام‌های صوتی).
              </p>
              <div className="edition-meta">
                <span>۱۵ فصل فیلم‌نامه</span>
                <span>رمان ۲۶۵ صفحه‌ای</span>
                <span>آرشیو پیام‌های صوتی</span>
                <span>۲۳ مأموریت فرعی</span>
              </div>
              <button
                type="button"
                className="edition-secondary-btn"
                onClick={(e) => {
                  e.stopPropagation();
                  switchEdition('v11');
                }}
              >
                ورود به نسخهٔ ۱۱
              </button>
            </article>
          </div>
          <div className="picker-footer">
            <button type="button" className="picker-logout" onClick={logout}>
              <LogOut size={16} /> خروج از مطالعه
            </button>
          </div>
        </section>
      </main>
    );

  if (!activeLib) return null;

  return (
    <div className={`app ${dark ? 'night-reader' : ''}`}>
      <aside className={`sidebar ${menu ? 'open' : ''}`}>
        <a
          className="brand"
          href="#"
          onClick={(e) => {
            e.preventDefault();
            navigate('home');
          }}
        >
          <span className="brand-symbol">ه</span>
          <span>
            ردِ هور<small>کتابِ طراحی و رمان</small>
          </span>
        </a>
        <div className="edition">
          <div className="edition-label">
            <strong>
              {isV13
                ? 'نسخهٔ ۱۳ · سنتزِ نهایی'
                : isV12
                  ? 'نسخهٔ ۱۲ · بین‌المللی'
                  : 'نسخهٔ ۱۱ · روایتِ بومی'}
            </strong>
            <span>
              {isV13
                ? 'مرجعِ قفل‌شده · Canon فعلی'
                : isV12
                  ? 'آرشیو · اکشنِ بین‌المللی'
                  : 'آرشیو · درامِ بومی AAA'}
            </span>
          </div>
          <div className="edition-toggle" role="group" aria-label="تغییر نسخه">
            <button type="button" className={isV13 ? 'active' : ''} onClick={() => switchEdition('v13')}>
              نسخهٔ ۱۳
            </button>
            <button type="button" className={isV12 ? 'active' : ''} onClick={() => switchEdition('v12')}>
              نسخهٔ ۱۲
            </button>
            <button type="button" className={!isModern ? 'active' : ''} onClick={() => switchEdition('v11')}>
              نسخهٔ ۱۱
            </button>
          </div>
        </div>
        <nav aria-label="بخش‌های اصلی">
          {navGroups.map(([group, ids]) => (
            <React.Fragment key={group}>
              <span className="nav-group">{group}</span>
              {ids.map((id) => {
                const item = labels.find((x) => x[0] === id)!;
                const [key, label, Icon] = item;
                return (
                  <button key={key} className={tab === key && !docId ? 'active' : ''} onClick={() => navigate(key)}>
                    <Icon size={20} />
                    {label}
                  </button>
                );
              })}
            </React.Fragment>
          ))}
        </nav>
        <div className="sidebar-bottom">
          <p>
            {isV13
              ? 'نام و ردپا در بیرون، دو قلهٔ وحشتِ Mk-1 در عمق.'
              : isV12
                ? 'لوتِ تاکتیکی در بیرون، وحشتِ Mk-1 در عمق.'
                : 'لوتِ خشن در بیرون، وحشتِ تنگه در عمق.'}
          </p>
          <span>ردِ هور · {editionLabel}</span>
          <button onClick={logout}>
            <LogOut size={17} />
            خروج از مطالعه
          </button>
        </div>
      </aside>
      {menu && <button className="menu-scrim" onClick={() => setMenu(false)} aria-label="بستن فهرست" />}
      <div className="workspace">
        <header className="topbar">
          <button className="icon-button mobile-menu" onClick={() => setMenu(!menu)} aria-label="باز کردن فهرست">
            <Menu />
          </button>
          <span className="breadcrumb">
            ردِ هور ({editionLabel}) <span>/</span> {activeTitle || labels.find((x) => x[0] === tab)?.[1]}
          </span>
          <div className="top-actions">
            <label className="search-box">
              <Search size={18} />
              <input
                aria-label="جستجو در همهٔ اسناد"
                placeholder="جستجو در داستان، مأموریت، سلاح، پهپاد…"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
              {query && (
                <button className="icon-button" onClick={() => setQuery('')} aria-label="پاک کردن جستجو">
                  <X size={16} />
                </button>
              )}
            </label>
            <button
              className="icon-button"
              onClick={() => setDark(!dark)}
              aria-label={dark ? 'مطالعه در زمینهٔ روشن' : 'مطالعه در زمینهٔ تیره'}
            >
              {dark ? <Sun size={19} /> : <Moon size={19} />}
            </button>
          </div>
        </header>
        <main id="main" className={doc ? 'document-main' : 'main-content'}>
          {query.trim().length >= 2 ? (
            <section className="section">
              <span className="eyebrow">جستجو در متن کامل · {editionLabel}</span>
              <h1>نتیجه برای «{query}»</h1>
              <p className="muted">{fa(searchResults.length)} سند یافت شد. نتایج ممکن است داستان را افشا کنند.</p>
              <div className="search-results">
                {searchResults.map((d) => (
                  <button key={d.id} onClick={() => openDoc(d.id, '', d.resultMode)}>
                    <span className="tag">{d.category}</span>
                    <small className="search-source">{d.sourceLabel}</small>
                    <h3>{d.title}</h3>
                    <p>{d.snippet}…</p>
                    <span className="text-link">خواندن سند</span>
                  </button>
                ))}
                {!searchResults.length && (
                  <div className="empty">نتیجه‌ای پیدا نشد؛ واژهٔ کوتاه‌تر یا املای دیگری را امتحان کنید.</div>
                )}
              </div>
            </section>
          ) : doc ? (
            <div className="document-layout">
              <aside className="toc">
                <button
                  className="text-link"
                  onClick={() => {
                    setDocId(null);
                    history.replaceState(null, '', new URL('./', document.baseURI).pathname);
                  }}
                >
                  بازگشت به {labels.find((x) => x[0] === tab)?.[1]}
                </button>
                <strong>در این سند</strong>
                <nav>
                  {toc
                    .filter((x) => x.level <= 3)
                    .map((x) => (
                      <a
                        key={x.id}
                        className={'level-' + x.level}
                        href={'#' + x.id}
                        onClick={(e) => {
                          e.preventDefault();
                          document.getElementById(x.id)?.scrollIntoView();
                        }}
                      >
                        {x.title}
                      </a>
                    ))}
                </nav>
              </aside>
              <article className="document">
                <div className="doc-meta">
                  <span className="tag">{doc.legacy ? 'آرشیو نسخه‌های قبل' : doc.category}</span>
                  <span>{fa(Math.ceil(activeMarkdown.split(/\s+/).length / 190))} دقیقه مطالعهٔ تقریبی</span>
                  <button className="icon-button" onClick={() => window.print()} aria-label="چاپ این سند">
                    <Printer size={19} />
                  </button>
                </div>
                {readerEdition && (
                  <nav className="reader-switch" aria-label="روش خواندن سند">
                    <a
                      className={summaryActive ? 'selected' : ''}
                      href={documentHref(doc.id, 'read')}
                      onClick={(e) => {
                        e.preventDefault();
                        openDoc(doc.id, '', 'read');
                      }}
                    >
                      توضیح ساده و روان
                    </a>
                    <a
                      className={viewMode === 'full' ? 'selected' : ''}
                      href={documentHref(doc.id, 'full')}
                      onClick={(e) => {
                        e.preventDefault();
                        openDoc(doc.id, '', 'full');
                      }}
                    >
                      متن کامل در نمایشگر Markdown
                    </a>
                    <span>{summaryActive ? 'خلاصهٔ روان همین سند' : 'متن کامل سند با فهرست و امکان چاپ'}</span>
                  </nav>
                )}
                {doc.legacy && (
                  <div className="notice warning">
                    <AlertCircle />
                    این سند آرشیوِ نسخه‌های قبلی است. مرجعِ رسمیِ فعلی اسنادِ {editionLabel} هستند.
                  </div>
                )}
                {doc.spoiler && !spoilers[doc.id] ? (
                  <div className="spoiler-gate">
                    <Eye size={32} />
                    <h1>{doc.title}</h1>
                    <p>این بخش شامل جزئیات پیشروی و پایان داستان است.</p>
                    <button className="primary" onClick={() => setSpoilers({ ...spoilers, [doc.id]: true })}>
                      نمایش متن کامل با افشای داستان
                    </button>
                  </div>
                ) : (
                  <RichText text={activeMarkdown} onNavigate={openFile} />
                )}
                <div className="end-note">
                  پایان سند · {doc.legacy ? 'آرشیو تاریخی' : editionTag}
                  <button className="text-link" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
                    بازگشت به ابتدای سند
                  </button>
                </div>
              </article>
            </div>
          ) : tab === 'home' ? (
            <>
              <section className="hero">
                <img src={media(heroImg)} alt="کانسپت‌آرتِ ردِ هور" />
                <div className="hero-shade" />
                <div className="hero-content">
                  <span className="eyebrow">
                    ردِ هور ·{' '}
                    {isV13
                      ? 'نسخهٔ ۱۳ · سنتزِ نهاییِ کانن'
                      : isV12
                        ? 'نسخهٔ ۱۲ · اکشنِ بین‌المللی'
                        : 'نسخهٔ ۱۱ · کویرِ لوت'}
                  </span>
                  <h1>{activeLib.copy.heroTitle}</h1>
                  <p className="logline">{activeLib.copy.heroText}</p>
                  <div className="button-row">
                    <button className="primary" onClick={() => navigate('read')}>
                      فیلم‌نامهٔ ۱۵ فصلی را بخوان
                    </button>
                    <button className="light-button" onClick={() => navigate('novel')}>
                      رمانِ کامل را بخوان
                    </button>
                  </div>
                  <div className="release-stamp" title="نسخهٔ محتوای بازی · انتشارِ سایت · شناسهٔ بیلد">
                    <b>
                      {edition} · {release.major}.{release.minor}.{release.patch}
                    </b>
                    <span>build {release.build}</span>
                  </div>
                </div>
                <span className="hero-caption">کانسپت‌آرتِ مطالعاتیِ ردِ هور</span>
              </section>
              <section className="section intro-video-section">
                <div className="section-heading">
                  <div>
                    <span className="eyebrow">اینتروی پیشنهادی · نسخهٔ اولیه (۱:۰۰)</span>
                    <h2>پیش‌درآمدِ تنگهٔ هور — هفت چراغ پیشانی</h2>
                    <p>
                      نسخهٔ آزمایشیِ ۱ دقیقه‌ای بر پایهٔ پیش‌درآمدِ شبِ تنگه (برای مرورِ لحن، ریتم و فضاسازیِ اولیه پیش
                      از ساختِ سکانسِ نهایی).
                    </p>
                  </div>
                  <span className="tag">۱:۰۰ · 1080p</span>
                </div>
                <div className="intro-video-frame">
                  <video
                    src={introUrl('rad-e-hoor-intro.mp4')}
                    poster={introUrl('poster.jpg')}
                    controls
                    playsInline
                    preload="metadata"
                  />
                </div>
              </section>
              <section className="section">
                <div className="section-heading">
                  <div>
                    <span className="eyebrow">شخصیت‌های اصلی و همراهان · {editionLabel}</span>
                    <h2>
                      {isV13
                        ? '۱۷ چهره با ترازوی «نام و ردپا»، ریتمِ گفتارِ اختصاصی و خاکستریِ واقعی'
                        : isV12
                          ? 'تیمِ عملیاتی، دلالِ بازارِ سیاه و خریدارانِ PMC'
                          : 'کسانی که در لوت می‌جنگند، می‌سوزند یا دردسر می‌سازند'}
                    </h2>
                  </div>
                  <button className="text-link" onClick={() => navigate('story')}>
                    همه را ببین ({fa(activeLib.people.length)} نفر)
                  </button>
                </div>
                <div className="cast-strip">
                  {activeLib.people.slice(0, 12).map((p) => (
                    <button key={p.name} className="cast-card" onClick={() => navigate('story')}>
                      {p.image ? (
                        <img src={media(p.image)} alt={'مرجع تصویری ' + p.name} loading="lazy" />
                      ) : (
                        <div className="cast-ph">
                          <Users size={28} />
                        </div>
                      )}
                      <strong>{p.name}</strong>
                      <span>{p.role}</span>
                      {p.quote && <em>«{p.quote}»</em>}
                    </button>
                  ))}
                </div>
              </section>
              <section className="section">
                <div className="section-heading">
                  <div>
                    <span className="eyebrow">پانزده فصل در ۶ پرده</span>
                    <h2>
                      {isV13
                        ? 'از کارگاهِ شهداد تا باندِ نمکزار، حجرهٔ رگه و درِ چوبیِ شهداد'
                        : isV12
                          ? 'از کارگاهِ شهداد تا باندِ پروازِ نمکزار و حجرهٔ رگه'
                          : 'از شهداد تا حجرهٔ رگه'}
                    </h2>
                  </div>
                  <button className="text-link" onClick={() => navigate('read')}>
                    شروع از پیش‌درآمد و فصل اول
                  </button>
                </div>
                <div className="chapter-cards">
                  {activeLib.chapters.map((c, i) => (
                    <button
                      key={c.number}
                      className="chapter-card"
                      onClick={() => {
                        setReadOk(true);
                        setReadIdx(i);
                        navigate('read');
                      }}
                    >
                      <span className="eyebrow">فصل {fa(c.number)}</span>
                      <h3>{c.title}</h3>
                      <p>
                        {(activeLib.chapterSummaries[i] || '').slice(0, 150)}
                        {(activeLib.chapterSummaries[i] || '').length > 150 ? '…' : ''}
                      </p>
                    </button>
                  ))}
                </div>
              </section>
              <section className="intro-strip">
                <div>
                  <span className="eyebrow">معماریِ جهانِ ردِ هور · {editionLabel}</span>
                  <h2>رمانِ کامل، سلاح و ورکشاپ، دفاع از پایگاه، سنگ‌نگاره‌ها و آبشخورها</h2>
                </div>
                <p>
                  کمپینِ ۳۰ تا ۴۰ ساعتهٔ نیمه‌باز در کویرِ لوت همراه با ۲ فصلِ نادر و هولناکِ وحشت در اعماقِ تنگهٔ هور.{' '}
                  <button className="text-link" onClick={() => navigate('novel')}>
                    رمانِ کامل، ۲۰ فصل و اپیلوگ
                  </button>{' '}
                  ·{' '}
                  {isV13 ? (
                    <>
                      <button className="text-link" onClick={() => openDoc('00_CANON_LEDGER_FA', '', 'full')}>
                        دفترِ کلِ کانن
                      </button>{' '}
                      ·{' '}
                      <button className="text-link" onClick={() => openDoc('05_GAMEPLAY_FA', '', 'full')}>
                        گیم‌پلی و مأموریت‌ها (M00–M40)
                      </button>{' '}
                      ·{' '}
                      <button className="text-link" onClick={() => openDoc('PLACES_OF_LOT_FA', '', 'full')}>
                        مکان‌ها، ناوگان و سلاح‌ها
                      </button>{' '}
                      ·{' '}
                      <button className="text-link" onClick={() => openDoc('DIRECTOR_PRINCIPLES_FA', '', 'full')}>
                        منشورِ کارگردانی و دمو
                      </button>
                    </>
                  ) : (
                    <>
                      <button
                        className="text-link"
                        onClick={() => openDoc('06_WEAPONS_CRAFTING_AND_WORKSHOP_FA', '', 'full')}
                      >
                        سلاح و ورکشاپ
                      </button>{' '}
                      ·{' '}
                      <button
                        className="text-link"
                        onClick={() => openDoc('07_CAMP_CARAVANSERAI_WORKSHOP_WATERHOLES_FA', '', 'full')}
                      >
                        مأموریت‌ها، پایگاه و سنگ‌نگاره‌ها
                      </button>{' '}
                      ·{' '}
                      <button
                        className="text-link"
                        onClick={() => openDoc('05_DIRECTION_MISE_EN_SCENE_AND_EASTER_EGGS_FA', '', 'full')}
                      >
                        کارگردانی و ۱۸ ایستر‌اگ
                      </button>
                    </>
                  )}
                </p>
              </section>
              <section className="review-panel">
                <h2>از خواننده چه نظری می‌خواهیم؟</h2>
                <p>
                  {isV13
                    ? 'سنتزِ نسخهٔ ۱۳ چطور بود؟ پیوندِ رازِ «سام» و پروندهٔ «مشتریِ د» با ساعتِ شنیِ پروازِ کروز، مکانیکِ فریادزدنِ اسم («هیراد!»)، مهارِ قابل‌بازیِ هواپیما با وینچِ ۱۰تُنی و اپیلوگِ شهداد چقدر یکپارچه است؟'
                    : isV12
                      ? 'لحنِ سرد و بین‌المللیِ v12 چطور بود؟ خطِ ۴۸ ساعتِ پاک‌شده، پویا (دلالِ دیوانه)، باندِ پروازِ نمکزار و پایانِ «سایت ۰۱» جواب داد؟'
                      : 'لحنِ دیالوگ‌های جدید چطور بود؟ توازنِ اکشنِ انسانی با ۲ فصلِ وحشتِ تنگه جواب داد؟ کدام وسیلهٔ نقلیه یا باس‌فایت قوی‌تر بود؟'}
                </p>
                <button
                  className="secondary"
                  onClick={async () => {
                    try {
                      await navigator.clipboard.writeText(
                        `بازخورد ردِ هور — ${editionTag}\nفصل / مأموریت:\nبهترین صحنه یا دیالوگ:\nبخش‌هایی که هنوز خام به نظر آمد:\nنظر دربارهٔ پهپاد/اپتیک/سلاح/وسایل نقلیه:\nپیشنهاد مشخص:`,
                      );
                      setReviewCopied(true);
                    } catch {
                      setReviewCopied(false);
                    }
                  }}
                >
                  {reviewCopied ? <Check size={17} /> : <BookOpen size={17} />}{' '}
                  {reviewCopied ? 'فرم نظر کپی شد' : 'کپی کردن قالب بازخورد'}
                </button>
              </section>
            </>
          ) : tab === 'overview' ? (
            <section className="section overview-section">
              <span className="eyebrow">راهنمای خواننده · پنج بخش · {editionLabel}</span>
              <h1>ایده و داستان کلی</h1>
              <p className="lead">
                یک مرور روشن از جهان، قهرمان‌ها، مسیر پانزده‌فصلی، مأموریت‌های اصلی و داستان‌های فرعی. این بخش خلاصهٔ
                داستان را تا پایان شرح می‌دهد و شامل افشای داستان است.
              </p>
              <nav className="overview-pages" aria-label="صفحه‌های ایده و داستان">
                {[
                  ['هستهٔ داستان', 'ایده، جهان و کشمکش'],
                  ['شخصیت‌ها', 'قهرمان‌ها و دشمن'],
                  ['مسیر کمپین', 'پانزده فصل'],
                  ['مأموریت‌های اصلی', `${fa(activeLib.budget.main_missions.length)} مأموریت`],
                  ['مأموریت‌های فرعی', `${fa(activeLib.sideStories.length)} زنجیره و فعالیت`],
                ].map(([title, sub], i) => (
                  <button
                    key={title}
                    className={overviewPage === i + 1 ? 'selected' : ''}
                    onClick={() => setOverviewPage(i + 1)}
                  >
                    <span>{fa(i + 1)}</span>
                    <strong>{title}</strong>
                    <small>{sub}</small>
                  </button>
                ))}
              </nav>
              <article className="overview-paper">
                {overviewPage === 1 ? (
                  <>
                    <span className="eyebrow">صفحهٔ ۱ · ایده، جهان و کشمکش · {editionLabel}</span>
                    <h2>ردِ هور در یک نگاه</h2>
                    {isV13 ? (
                      <>
                        <p>
                          «ردِ هور» (نسخهٔ ۱۳ — سنتزِ نهاییِ کانن) یک اکشن-تریلرِ تاکتیکی و انسانیِ نیمه‌جهان‌باز در کویرِ
                          لوت است که بر قاعدهٔ آهنینِ <strong>«نام و ردپا»</strong> بنا شده است: دانیال — راننده-مکانیکِ
                          کامیونِ ده‌تُنیِ «پیرمرد» با زخمِ پنهانِ تصادفِ سامِ هشت‌ساله و دو سال سکوت در برابرِ بردنِ چهار
                          کارگرِ دست‌بسته — همراهِ سارا (بازرسِ بیمه‌ای که قراردادِ ۴۰۰هزار دلاری‌اش فقط «تحویلِ سالمِ نمونه»
                          را مجاز دانسته) در برابرِ شبکهٔ فراموشیِ کامران و ساعتِ شنیِ ۶روزهٔ پروازِ <strong>ویکتور کروز</strong>{' '}
                          (<code>Kestrel Logistics</code>) می‌ایستد.
                        </p>
                        <p>
                          زیست-کانیِ <strong>H-0</strong> روی چهار نمودِ دقیق قفل شده است (گازِ خامِ <code>دَمِ هور</code>،{' '}
                          <code>Mk-1</code> در دو قلهٔ وحشتِ فصل ۶ و ۱۲ با مکانیکِ فریادزدنِ اسم، آمپولِ <code>H-0 Wipe</code> و
                          نگهبانانِ بی‌نامِ <code>Mk-2</code> — با حذفِ کاملِ <code>Mk-3</code>). از پیدایشِ سه‌لایهٔ{' '}
                          <strong>درایوِ کیان</strong> در پایانِ فصل ۲ تا افشای یگانهٔ پروندهٔ <strong>«مشتریِ د»</strong> در
                          فصل ۱۰، خیانتِ بهرام در برجِ رادیو و مرگش در آشیانهٔ نمکزار، مهارِ ۱۰۰٪ قابل‌بازیِ هواپیما با وینچِ
                          ۱۰تُنیِ «پیرمرد» و اپیلوگِ کوبیدنِ درِ چوبیِ خانهٔ مادرِ سام در شهداد، هیچ سرنخی بی‌برداشت رها نمی‌شود.
                        </p>
                      </>
                    ) : isV12 ? (
                      <>
                        <p>
                          «ردِ هور» (نسخهٔ ۱۲) یک اکشن-تریلرِ تاکتیکیِ نیمه‌جهان‌باز در کویرِ لوت با ستون‌های لحنی{' '}
                          <strong>MGSV + Mad Max + Sicario + RE4</strong> است. دانیال — فرماندهٔ سابقِ کاروان‌ها و
                          عملیاتِ سیاه — با یک زخمِ گلوله و ۴۸ ساعت حافظهٔ پاک‌شده، همراه با سارا (زیست-زمین‌شناسِ
                          مستقل) و تیمِ عملیاتیِ کمپ در برابرِ برنامهٔ تسلیحاتیِ کامران می‌ایستد. کامران زیرِ پوششِ
                          نیروگاهِ خورشیدی و معدنِ لیتیوم، از رگهٔ بی‌هوازیِ <strong>H-0</strong> سلاحِ عصبی-زیستی
                          (نسل‌های Mk-1 و Mk-2) برای فروش به شرکت‌های نظامیِ خصوصی (PMC) می‌سازد.
                        </p>
                        <p>
                          داستان از نشتِ عمدیِ هفت سال پیش در گسل و فرارِ کاوه شروع می‌شود. در ادامه، درایوِ رمزگذاری‌شدهٔ
                          ۴۸ ساعت، معاملهٔ ویکتور کروز (خریدارِ بین‌المللیِ PMC)، بازارِ سیاهِ پویا در «کلوتِ لاشه‌ها» و
                          باندِ پروازِ مخفیِ نمکزار همه به یک خطِ مستقیمِ اکشن گره می‌خورند — بدونِ ملودرام، درامِ
                          خانوادگی یا سیاست.
                        </p>
                      </>
                    ) : (
                      <>
                        <p>
                          «ردِ هور» یک بازی اکشن و ماجراییِ نیمه‌باز در لوت است. دانیال، راننده و مکانیکی که گذشته‌ای
                          پرمسئله دارد، همراه سارا و گروهی کوچک از مردم منطقه در برابر شبکهٔ کامران می‌ایستد. کامران زیر
                          پوشش یک پروژهٔ معدنی و نیروگاه خورشیدی، از گاز و رطوبتِ یک گسل برای ساخت ماده‌ای استفاده می‌کند
                          که حافظه را مختل می‌کند.
                        </p>
                        <p>
                          داستان از یک حادثهٔ قدیمی در کارگاه و ناپدیدشدن شش کارگر شروع می‌شود. سال‌ها بعد، سرنخ‌ها از
                          جاده و کمپ به نیروگاه و تأسیسات زیرزمینی می‌رسند. دانیال باید هم رازِ آن حادثه را کشف کند و هم
                          جلوی تکرار آن را بگیرد؛ در حالی که روشن می‌شود تصمیم‌ها و سکوت‌های گذشتهٔ خودش نیز به این زنجیره
                          آسیب زده‌اند.
                        </p>
                      </>
                    )}
                    <h3>راه‌یابی در شب</h3>
                    <p>
                      در آموزشِ نخستین شبِ کمپ (M06)، بازیکن دبِ اکبر را پیدا می‌کند و امتدادِ ستاره‌های راهنما را تا
                      ستارهٔ قطبی می‌گیرد؛ اگر این صورت فلکی پایین افق باشد، ذات‌الکرسی نشانهٔ جایگزین است. سپس نقشهٔ
                      کاغذی را رو به شمال تنظیم می‌کند و با خطِ‌الرأس و آبراههٔ خشک، مسیر بازگشت را خودش انتخاب می‌کند.
                      ابر و غبار راه‌یابی را به قطب‌نما و نشانه‌های زمینی می‌سپارند؛ راهنمای بازی هم اختیاری می‌ماند.
                    </p>
                    <h3>کمپ و دوام‌آوردن در کویر</h3>
                    <p>
                      بازیکن پیش از تاریکی برای شب‌مانی جای امنی انتخاب می‌کند، آب و خوراک و قطعات لازم را به کمپ
                      می‌رساند و در صورت تمایل کنارِ درختِ تنها آتش کوچکی برپا می‌کند. استراحت بخشی از استقامت را
                      برمی‌گرداند و بسته به وضعیت کمپ، گفت‌وگوی همراهان یا نوای کمانچهٔ کاوه را به همراه دارد. در
                      روزهای سخت، سایه و آب محدودند؛ گرما و طوفان شن روی حرکت و آماده‌بودن تجهیزات اثر می‌گذارند.
                    </p>
                    <h3>سراب و خطای دید در گرما</h3>
                    <p>
                      سرابِ واقعیِ ظهر، آب یا کاروانی را در افق نشان می‌دهد و با نزدیک‌شدن محو می‌شود. اگر بازیکن مصرفِ
                      آب یا غذا را در گرمای شدید نادیده بگیرد، تاریِ دید و موجِ تصویر تشخیصِ سراب را دشوارتر می‌کند.
                      بازیکن با نوشیدن یا خوردن، رفتن به سایه و سنجیدنِ خطِ زمین با نقشه دیدش را برمی‌گرداند. این
                      افکت‌ها قابلِ کاهش یا خاموش‌کردن‌اند.
                    </p>
                    <div className="two-cards">
                      <button
                        className="path-card"
                        onClick={() =>
                          openDoc(isV13 ? 'PLACES_OF_LOT_FA' : '04_OPEN_WORLD_SYSTEMS_AND_VISUAL_BIBLE_FA', '', 'full')
                        }
                      >
                        <h3>راه‌یابی شبانه و تجربهٔ جهان</h3>
                        <p>آموزش ستاره‌یابی، نقشه‌خوانی، نشانه‌های طبیعی و زندگیِ نیمه‌باز در لوت.</p>
                        <span className="text-link">خواندن سند کامل</span>
                      </button>
                      <button
                        className="path-card"
                        onClick={() =>
                          openDoc(
                            isV13 ? '05_GAMEPLAY_FA' : '07_CAMP_CARAVANSERAI_WORKSHOP_WATERHOLES_FA',
                            '',
                            'full',
                          )
                        }
                      >
                        <h3>کمپ، آبشخور و نگهداری</h3>
                        <p>زندگی روزمرهٔ کمپ، فعالیت‌های اختیاری، آب، غذا، برق و تعمیرات.</p>
                        <span className="text-link">خواندن سند کامل</span>
                      </button>
                    </div>
                    <div className="notice warning">
                      <Eye size={18} />
                      {isV13
                        ? 'این مرور پایان داستان را لو می‌دهد: در فصل ۱۵ دانیال در حجرهٔ رگه ویالِ فراموشیِ کامران را می‌شکند («اسمش سام بود»)، روی باندِ نمکزار با وینچِ ۱۰تُنیِ «پیرمرد» و شلیکِ RPG هواپیمای کروز را منهدم می‌کند، پاکت را برای ۱۰ خانواده می‌سپارد و در اپیلوگِ شهداد درِ خانهٔ مادرِ سام را می‌زند.'
                        : isV12
                          ? 'این مرور پایان داستان را لو می‌دهد: در فصل ۱۵ دانیال پس از نبردِ دوفاز با کامران در حجرهٔ رگه و انهدامِ هواپیمای باربریِ ویکتور کروز در باندِ نمکزار، با فایلِ «سایت ۰۱» روبه‌رو می‌شود و در سپیده به دلِ جادهٔ بازِ لوت می‌زند.'
                          : 'این مرور پایان داستان را لو می‌دهد: در سکانس نهایی، دانیال در دوئلی رو در رو با کامران مواجه می‌شود و باید دربارهٔ عدالت، انتقام و زنده‌ماندن دیگران تصمیم بگیرد.'}
                    </div>
                  </>
                ) : overviewPage === 2 ? (
                  <>
                    <span className="eyebrow">صفحهٔ ۲ · شخصیت‌ها و کشمکش</span>
                    <h2>آدم‌هایی با خواسته‌های جداگانه</h2>
                    <p>
                      {isV13
                        ? 'در نسخهٔ ۱۳ هر یک از ۱۷ شخصیت ریتمِ گفتار، تیکِ رفتاری و شیءِ داستانیِ اختصاصیِ خود را دارد: سارا میانِ قراردادِ ۴۰۰هزار دلاریِ «تحویلِ سالم» و انهدامِ محموله می‌ایستد؛ کاوه بارِ شش نام و دریچهٔ سعید را دارد؛ رامین مغزِ فنی و گرمِ کارگاه است؛ پویا با لاگرِ پنهانِ باتری کمپِ ۱ را لو می‌دهد؛ بهرام برای صندلیِ پرواز رامین را می‌فروشد؛ و سورن با دیدنِ امضای ناخوانایش علیه کامران می‌شورد.'
                        : isV12
                          ? 'داستان بر یک تیمِ عملیاتیِ کم‌حرف و کارکشته تکیه دارد: سارا با آنالیزِ شیمیایی و کارابین پیش می‌رود؛ کاوه تنها بازماندهٔ نشتِ هفت سال پیش است؛ رامین پهپاد، NVG و EMP می‌سازد؛ مینا نبکاها را ردیابی می‌کند؛ رویا زرادخانهٔ کاروانسرا را در اختیار دارد؛ پویا دلالِ دیوانهٔ «کلوتِ لاشه‌ها» است؛ و سورن پس از کشفِ دوزِ پنهانِ H-0 در جیرهٔ خودش، روی پل علیه کامران شورش می‌کند.'
                          : 'داستان بر گروهی متکی است که هر کدام مهارت و انگیزهٔ خود را دارند. سارا با مدرک و تحلیل زمین‌شناسی پیش می‌رود؛ کاوه بارِ خاطره و فقدانِ کارگران را دارد؛ رامین کارگاه و وسایل را سرپا نگه می‌دارد؛ مینا از حیات‌وحش و آبشخورها مراقبت می‌کند؛ رویا شبکهٔ رانندگان و مسیرهای غیررسمی را می‌شناسد؛ و سورن از درونِ نیروهای کامران با حقیقت روبه‌رو می‌شود.'}
                    </p>
                    <div className="overview-people">
                      {activeLib.people.slice(0, 12).map((p) => (
                        <article key={p.name}>
                          <strong>{p.name}</strong>
                          <span>{p.role}</span>
                          <p>{p.text}</p>
                        </article>
                      ))}
                    </div>
                    <button className="secondary" onClick={() => navigate('story')}>
                      دیدن همهٔ شخصیت‌ها و تصویرها
                    </button>
                  </>
                ) : overviewPage === 3 ? (
                  <>
                    <span className="eyebrow">صفحهٔ ۳ · مسیر کمپین</span>
                    <h2>پانزده فصل از شهداد تا تنگه</h2>
                    <p>
                      کمپین در شش ناحیهٔ پیوسته پیش می‌رود. هر فصل دسترسی تازه‌ای می‌دهد و بخشی از راز را روشن می‌کند؛
                      ناحیه‌ها به مسیرهای فرعی و حلقه‌های اکتشاف وصل‌اند.
                    </p>
                    <div className="overview-chapters">
                      {activeLib.chapters.map((c, i) => (
                        <article key={c.number}>
                          <span className="mission-id">فصل {fa(c.number)}</span>
                          <div>
                            <h3>{c.title}</h3>
                            <p>{activeLib.chapterSummaries[i]}</p>
                          </div>
                          <span className="tag">{fa(c.minutes)} دقیقهٔ هدف</span>
                        </article>
                      ))}
                    </div>
                    <button
                      className="secondary"
                      onClick={() => {
                        setReadOk(true);
                        navigate('read');
                      }}
                    >
                      ورود به فیلم‌نامهٔ فصل‌به‌فصل
                    </button>
                  </>
                ) : overviewPage === 4 ? (
                  <>
                    <span className="eyebrow">صفحهٔ ۴ · مأموریت‌های اصلی</span>
                    <h2>{fa(activeLib.budget.main_missions.length)} مأموریت در دلِ داستان</h2>
                    <p>
                      مأموریت‌های اصلی، جست‌وجوی پاسخ را به کنش تبدیل می‌کنند: تعقیب و ردیابی، نفوذ مخفیانه، درگیری
                      مسلحانه، نجات همراهان و رویارویی با دشمنان مهم. چهار رخداد D01 تا D04 نیز وضعیت رادیو، خودرو، درا
                      و ذخایر کمپ را در ادامهٔ بازی تغییر می‌دهند.
                    </p>
                    <div className="overview-main-missions">
                      {activeLib.chapters.map((c) => {
                        const missions = activeLib.budget.main_missions.filter((m: any) => m.chapter === c.number);
                        return missions.length ? (
                          <details key={c.number}>
                            <summary>
                              <span>
                                فصل {fa(c.number)} · {c.title}
                              </span>
                              <small>{fa(missions.length)} مأموریت</small>
                            </summary>
                            <div>
                              {missions.map((m: any) => (
                                <article key={m.id}>
                                  <span className="mission-id" dir="ltr">
                                    {m.id}
                                  </span>
                                  <div>
                                    <strong>{m.title_fa}</strong>
                                    <p>{m.focus_tags_fa?.join(' · ') || 'پیشبرد داستان و اکشن'}</p>
                                  </div>
                                  <span className="tag">{fa(m.minutes)} دقیقه</span>
                                </article>
                              ))}
                            </div>
                          </details>
                        ) : null;
                      })}
                    </div>
                  </>
                ) : (
                  <>
                    <span className="eyebrow">صفحهٔ ۵ · مأموریت‌های فرعی</span>
                    <h2>
                      {isModern ? 'عملیات‌های جانبی، بازارِ سیاهِ پویا و دفاع از پایگاه' : 'داستان‌های کوچکِ لوت'}
                    </h2>
                    <p>
                      {fa(activeLib.sideStories.length)} مأموریت و معمای فرعی به بازیکن اجازه می‌دهند پیش از ادامهٔ خط
                      اصلی به تیم، تجهیزات و اکتشاف بپردازد. بسیاری از آن‌ها پاداشِ عملی، تسلیحاتی یا اطلاعاتی می‌دهند
                      اما اجباری نیستند.
                    </p>
                    <div className="overview-side-missions">
                      {activeLib.sideStories.map((s) => (
                        <details key={s.id}>
                          <summary>
                            <span className="mission-id" dir="ltr">
                              {s.id}
                            </span>
                            <strong>{s.title}</strong>
                            <span>جزئیات</span>
                          </summary>
                          <RichText text={s.markdown} onNavigate={openFile} />
                        </details>
                      ))}
                    </div>
                    <button className="secondary" onClick={() => navigate('missions')}>
                      رفتن به فهرست قابل‌فیلتر مأموریت‌ها
                    </button>
                  </>
                )}
              </article>
              <div className="reader-pager">
                <button
                  className="secondary"
                  disabled={overviewPage <= 1}
                  onClick={() => setOverviewPage(overviewPage - 1)}
                >
                  <ChevronRight size={18} /> صفحهٔ قبل
                </button>
                <span>{fa(overviewPage)} از ۵</span>
                <button
                  className="secondary"
                  disabled={overviewPage >= 5}
                  onClick={() => setOverviewPage(overviewPage + 1)}
                >
                  صفحهٔ بعد <ChevronLeft size={18} />
                </button>
              </div>
            </section>
          ) : tab === 'read' ? (
            <section className="section reader-section">
              {!readOk ? (
                <div className="spoiler-gate">
                  <BookOpen size={32} />
                  <h1>فیلم‌نامهٔ کاملِ ردِ هور ({editionLabel})</h1>
                  <p>
                    پیش‌درآمد، ۱۵ فصل و اپیلوگ را با دیالوگ‌های زنده و سکانس‌های اکشن و وحشت بخوانید.
                  </p>
                  <button className="primary" onClick={() => setReadOk(true)}>
                    شروع خواندن
                  </button>
                </div>
              ) : story ? (
                <>
                  <div className="script-intro">
                    <div>
                      <span className="eyebrow">فیلم‌نامهٔ بازی · {editionLabel}</span>
                      <h1>روایتِ صحنه‌به‌صحنه</h1>
                      <p>هر فصل را جدا بخوانید؛ عنوانِ صحنه‌ها، کنش، میزانسن و دیالوگ‌ها قالب‌بندی شده‌اند.</p>
                    </div>
                    <div className="script-facts">
                      <span>
                        <b>{fa(story.chapters.length)}</b> بخش
                      </span>
                      <span>
                        <b>
                          {fa(
                            story.chapters.reduce((n, c) => n + (c.match(/^\*\*نما\s*[\d۰-۹]+/gm) || []).length, 0),
                          )}
                        </b>{' '}
                        صحنه
                      </span>
                      <button className="secondary" onClick={() => openDoc(screenplayDocId, '', 'full')}>
                        متن کامل و پیوسته
                      </button>
                    </div>
                  </div>
                  <div className="reader-layout">
                    <nav className="reader-nav" aria-label="فصل‌های داستان">
                      <strong>فصل‌ها</strong>
                      {story.chapters.map((c, i) => (
                        <button
                          key={i}
                          className={i === readIdx ? 'selected' : ''}
                          onClick={() => {
                            setReadIdx(i);
                            window.scrollTo({ top: 0 });
                          }}
                        >
                          {c.split('\n')[0].replace(/^## /, '').replace(' ★', '')}
                        </button>
                      ))}
                    </nav>
                    <article className="reader">
                      {(() => {
                        const c = story.chapters[Math.min(Math.max(readIdx, 0), story.chapters.length - 1)];
                        const head = c.split('\n')[0].replace(/^## /, '');
                        const [num, ...ttl] = head.split(' — ');
                        const img =
                          chapterImages[readIdx] && activeLib.gallery.some((g) => g.id === chapterImages[readIdx])
                            ? chapterImages[readIdx]
                            : null;
                        return (
                          <>
                            <span className="eyebrow">{num}</span>
                            <h1>{ttl.join(' — ')}</h1>
                            {img && (
                              <figure className="chapter-hero">
                                <img src={media(img)} alt="تصویر مفهومی فصل" loading="lazy" />
                                <figcaption>تصویر مفهومیِ فضای فصل</figcaption>
                              </figure>
                            )}
                            <RichText text={c.split('\n').slice(1).join('\n')} story onNavigate={openFile} />
                          </>
                        );
                      })()}
                      <div className="reader-pager">
                        <button
                          className="secondary"
                          disabled={readIdx <= 0}
                          onClick={() => {
                            setReadIdx(readIdx - 1);
                            window.scrollTo({ top: 0 });
                          }}
                        >
                          <ChevronRight size={18} /> فصل قبل
                        </button>
                        <span>{`${fa(readIdx + 1)} از ${fa(story.chapters.length)}`}</span>
                        <button
                          className="secondary"
                          disabled={readIdx >= story.chapters.length - 1}
                          onClick={() => {
                            setReadIdx(readIdx + 1);
                            window.scrollTo({ top: 0 });
                          }}
                        >
                          فصل بعد <ChevronLeft size={18} />
                        </button>
                      </div>
                    </article>
                  </div>
                </>
              ) : (
                <div className="empty">متن داستان در این بسته پیدا نشد.</div>
              )}
            </section>
          ) : tab === 'novel' ? (
            <section className="section reader-section novel-section">
              {!novelOk ? (
                <div className="spoiler-gate">
                  <BookOpen size={32} />
                  <span className="eyebrow">رمانِ کامل · ۲۰ فصل و اپیلوگ · {editionLabel}</span>
                  <h1>ردِ هور</h1>
                  <p>
                    {isV13
                      ? 'رمانِ اکشن-تریلرِ ادبیِ نسخهٔ ۱۳ در سه بخش (۲۰ فصل و اپیلوگ) روایت می‌شود؛ از هفت چراغ در عمقِ گسل تا مهارِ هواپیمای کروز روی نمکزار و درِ چوبیِ خانهٔ مادرِ سام در شهداد.'
                      : isV12
                        ? 'رمانِ اکشن-تریلرِ نسخهٔ ۱۲ در سه بخش روایت می‌شود؛ از نشتِ هفت‌سالهٔ تنگه تا باندِ پروازِ نمکزار و پایانِ سردِ «سایت ۰۱».'
                        : 'رمان در سه بخش روایت می‌شود؛ از فاجعهٔ هفت سال پیش تا رویاروییِ سپیده‌دم در تنگهٔ هور. متن زیر فصل‌به‌فصل پیش می‌رود تا جای روایت و زمان هر فصل روشن بماند.'}
                  </p>
                  <button className="primary" onClick={() => setNovelOk(true)}>
                    شروع خواندن
                  </button>
                </div>
              ) : novel?.length ? (
                <>
                  <div className="novel-intro">
                    <div>
                      <span className="eyebrow">
                        {editionLabel} · {fa(novel.length - 1)} فصل و اپیلوگ
                      </span>
                      <h1>رمانِ ردِ هور</h1>
                      <p>
                        حدودِ {fa(Math.ceil(novel.reduce((n, c) => n + c.words, 0) / 280))} صفحه با معیارِ تقریبیِ ۲۸۰
                        واژه در هر صفحه · مطالعهٔ فصل‌به‌فصل
                      </p>
                    </div>
                    <button className="secondary" onClick={() => openDoc(novelDocId, '', 'full')}>
                      نمایشِ متنِ پیوستهٔ Markdown
                    </button>
                  </div>
                  <div className="novel-layout">
                    <nav className="novel-nav" aria-label="فصل‌های رمان">
                      {[...new Set(novel.map((c) => c.part))].map((part) => (
                        <section key={part}>
                          <strong>{part}</strong>
                          {novel.map((c, i) =>
                            c.part === part ? (
                              <button
                                key={c.title}
                                className={i === novelIdx ? 'selected' : ''}
                                onClick={() => {
                                  setNovelIdx(i);
                                  window.scrollTo({ top: 0, behavior: 'smooth' });
                                }}
                              >
                                {c.title}
                              </button>
                            ) : null,
                          )}
                        </section>
                      ))}
                    </nav>
                    <article className="novel-reader">
                      {(() => {
                        const c = novel[Math.min(Math.max(novelIdx, 0), novel.length - 1)];
                        const mins = Math.max(1, Math.ceil(c.words / 220));
                        const date = c.date;
                        return (
                          <>
                            <span className="eyebrow">{c.part}</span>
                            <h2>{c.title}</h2>
                            {date && (
                              <p className="novel-meta">
                                {date} <span>·</span> حدودِ {fa(mins)} دقیقه مطالعه
                              </p>
                            )}
                            <RichText text={c.markdown} />
                          </>
                        );
                      })()}
                      <div className="reader-pager">
                        <button
                          className="secondary"
                          disabled={novelIdx <= 0}
                          onClick={() => {
                            setNovelIdx(novelIdx - 1);
                            window.scrollTo({ top: 0, behavior: 'smooth' });
                          }}
                        >
                          <ChevronRight size={18} /> فصلِ قبل
                        </button>
                        <span>
                          {fa(novelIdx + 1)} از {fa(novel.length)} بخش
                        </span>
                        <button
                          className="secondary"
                          disabled={novelIdx >= novel.length - 1}
                          onClick={() => {
                            setNovelIdx(novelIdx + 1);
                            window.scrollTo({ top: 0, behavior: 'smooth' });
                          }}
                        >
                          بخشِ بعد <ChevronLeft size={18} />
                        </button>
                      </div>
                    </article>
                  </div>
                </>
              ) : (
                <div className="empty">متن رمان در این بسته پیدا نشد.</div>
              )}
            </section>
          ) : tab === 'story' ? (
            <section className="section">
              <span className="eyebrow">{editionLabel} · هستهٔ شخصیت‌ها</span>
              <h1>آدم‌ها پیش از معما</h1>
              <p className="lead">{activeLib.copy.storyLead}</p>
              <div className="people-grid">
                {activeLib.people.map((p) => (
                  <article className="person" key={p.name}>
                    {p.image ? (
                      <button
                        className="person-image-button"
                        onClick={() => setLightbox(p.image)}
                        aria-label={'نمایش کامل تصویر ' + p.name}
                      >
                        <img src={media(p.image)} alt={'مرجع تصویری ' + p.name} loading="lazy" />
                      </button>
                    ) : (
                      <div className="person-placeholder">
                        <Users size={46} />
                        <span>در انتظارِ کانسپت {editionLabel}</span>
                      </div>
                    )}
                    <div>
                      <span className="eyebrow">{p.role}</span>
                      <h2>
                        {p.name}
                        <small>{fa(p.age)} ساله</small>
                      </h2>
                      <p>{p.text}</p>
                      {p.quote && <blockquote className="person-quote">«{p.quote}»</blockquote>}
                    </div>
                  </article>
                ))}
              </div>
              <div className="two-cards">
                <button
                  className="path-card"
                  onClick={() =>
                    openDoc(isV13 ? '02_CHARACTERS_FA' : '02_CHARACTERS_AND_DIALOGUE_CRAFT_FA', '', 'full')
                  }
                >
                  <h3>شخصیت‌ها و استانداردِ دیالوگ ({edition})</h3>
                  <p>
                    {isV13
                      ? 'بلوک‌های ۷خطیِ هر ۱۷ شخصیت، ریتمِ گفتارِ اختصاصی، پراپ‌های حاملِ داستان و مرزهای دانایی.'
                      : isV12
                        ? 'هستهٔ عملیاتیِ ۱۰ نفره + پویا و ویکتور کروز، قواعدِ دیالوگِ سرد و سه صحنهٔ نمونه.'
                        : 'روان‌شناسیِ هستهٔ ۱۰ نفره، قواعدِ دیالوگِ زنده و دو صحنهٔ نمونه.'}
                  </p>
                  <span className="text-link">خواندن سند</span>
                </button>
                <button className="path-card" onClick={() => openDoc(screenplayDocId, '', 'full')}>
                  <h3>فیلم‌نامهٔ کاملِ ۱۵ فصلی</h3>
                  <p>
                    {isV13
                      ? 'پیش‌درآمد (هفت چراغ)، ۱۵ فصل، ۵ باس‌فایت، مهارِ هواپیما با وینچ و اپیلوگِ درِ چوبیِ شهداد.'
                      : isV12
                        ? 'پیش‌درآمد، ۱۵ فصل، ۵ باس‌فایت و اپیلوگِ سردِ «سایت ۰۱».'
                        : 'پیش‌درآمد، ۱۵ فصل، ۵ باس‌فایت و اپیلوگِ شهداد.'}
                  </p>
                  <span className="text-link">ورود با هشدار افشای داستان</span>
                </button>
              </div>
            </section>
          ) : tab === 'places' ? (
            <section className="section places-page">
              <span className="eyebrow">راهنمای جغرافیا · جهانِ نیمه‌باز · {editionLabel}</span>
              <h1>محل‌ها</h1>
              <p className="lead">
                کجا در جغرافیای واقعیِ لوت ریشه دارد و کدام بخش برای داستان ساخته شده است؟ این صفحه مرزِ این دو را روشن
                می‌کند.
              </p>
              <div className="director-callout">
                <strong>راهنمای نقشه</strong>
                <p>
                  شهداد، نبکاها و کلوت‌ها الهامِ جغرافیاییِ واقعی‌اند. کاروانسرا، نیروگاهِ کامران، کمپ‌ها
                  {isModern ? '، آشیانه و باندِ پروازِ نمکزار' : ''} و تنگهٔ هور محل‌های داستانی هستند.
                </p>
                <button className="secondary" onClick={() => navigate('maps')}>
                  دیدنِ نقشه‌ها
                </button>
              </div>
              <RichText
                text={
                  activeLib.docs.find((d) => d.id === 'PLACES_OF_LOT_FA')?.markdown ||
                  'راهنمای محل‌ها در این نسخه موجود نیست.'
                }
              />
              <button className="secondary" onClick={() => openDoc('PLACES_OF_LOT_FA', '', 'full')}>
                باز کردن سندِ کامل
              </button>
            </section>
          ) : tab === 'direction' ? (
            <section className="section director-page">
              <span className="eyebrow">راهنمای تولید · {editionLabel}</span>
              <h1>اصول کارگردانی</h1>
              <p className="lead">یک قرارداد روشن برای روایت، دوربین، کنش، تصویر، صدا و بازنماییِ فرهنگِ لوت.</p>
              <div className="director-callout">
                <strong>قاعدهٔ مرکزی</strong>
                <p>هر انتخاب باید از دلِ جغرافیا و کنشِ بازیکن بیرون بیاید و پیامدش در جهان دیده شود.</p>
              </div>
              <RichText
                text={
                  activeLib.docs.find((d) => d.id === 'DIRECTOR_PRINCIPLES_FA')?.markdown ||
                  'سندِ اصول کارگردانی در این نسخه موجود نیست.'
                }
              />
              <button className="secondary" onClick={() => openDoc('DIRECTOR_PRINCIPLES_FA', '', 'full')}>
                باز کردن سندِ کامل
              </button>
            </section>
          ) : tab === 'dialogues' ? (
            <section className="section dialogue-section">
              <span className="eyebrow">دیالوگ‌های زندهٔ {editionLabel}</span>
              <h1>گفت‌وگوهای نوشته‌شده</h1>
              <p className="lead">
                {isV13
                  ? 'گفت‌وگوهای پیش‌درآمد، ۱۵ فصل و اپیلوگ را فصل‌به‌فصل بخوانید؛ زیرمتن‌محور، شیءمحور و با صدای متمایزِ هر شخصیت در نسخهٔ ۱۳.'
                  : isV12
                    ? 'گفت‌وگوهای هر ۱۵ فصل را جداگانه بخوانید. دیالوگ‌ها در نسخهٔ ۱۲ سرد، کوتاه، تاکتیکی و بدونِ ملودرام‌اند.'
                    : 'گفت‌وگوهای هر ۱۵ فصل را جداگانه بخوانید. دیالوگ‌ها با لحنِ زنده، تند و خاکی برای نسخهٔ ۱۱ بازنویسی شده‌اند.'}
              </p>
              <div className="notice">
                <Eye size={20} />
                گفت‌وگوهای فصل‌های میانی و پایانی، رازها و پایان داستان را آشکار می‌کنند.
              </div>
              {activeLib.dialogues?.note && <p className="dialogue-note">{activeLib.dialogues.note}</p>}
              {hasRecordings && (
                <div className="segmented">
                  {[
                    ['scenes', `گفت‌وگوهای ۱۵ فصل (${edition})`],
                    ['recordings', 'آرشیوِ پیام‌های صوتی'],
                  ].map(([id, title]) => (
                    <button key={id} className={dialogueMode === id ? 'selected' : ''} onClick={() => setDialogueMode(id)}>
                      {title}
                    </button>
                  ))}
                </div>
              )}
              {!hasRecordings || dialogueMode === 'scenes' ? (
                <>
                  <div className="chapter-selector">
                    {activeLib.chapters.map((c) => (
                      <button
                        key={c.number}
                        className={dialogueChapter === c.number ? 'selected' : ''}
                        onClick={() => setDialogueChapter(c.number)}
                      >
                        فصل {fa(c.number)}
                      </button>
                    ))}
                  </div>
                  <div className="chapter-intro">
                    <span className="eyebrow">فصل {fa(dialogueChapter)}</span>
                    <h2>{dialogue?.title || activeLib.chapters[dialogueChapter - 1]?.title}</h2>
                  </div>
                  <div className="dialogue-scenes">
                    {dialogue?.scenes.length ? (
                      dialogue.scenes.map((scene) => (
                        <article className="dialogue-scene" key={scene.id}>
                          <header>
                            <h3>{scene.title}</h3>
                            <p>{scene.context}</p>
                          </header>
                          <dl className="dialogue-lines">
                            {scene.lines.map((line, i) => (
                              <div key={i}>
                                <dt>{line.speaker}</dt>
                                <dd>{line.text}</dd>
                              </div>
                            ))}
                          </dl>
                          <footer>
                            <span className="muted" dir="ltr">
                              {scene.id}
                            </span>
                            <a
                              className="text-link"
                              href={documentHref(scene.source.docId, 'full', scene.source.section)}
                              onClick={(e) => {
                                e.preventDefault();
                                openDoc(scene.source.docId, scene.source.section, 'full');
                              }}
                            >
                              خواندن صحنه در متن کامل
                            </a>
                          </footer>
                        </article>
                      ))
                    ) : (
                      <div className="empty">برای این فصل گفت‌وگویی ثبت نشده است.</div>
                    )}
                  </div>
                </>
              ) : (
                <div className="recording-list">
                  <p className="dialogue-note">آرشیوِ متنِ پیام‌های صوتیِ نسخه‌های قبلی برای ارجاع.</p>
                  {activeLib.dialogues?.recordings.map((recording) => (
                    <details key={recording.id}>
                      <summary>
                        <MessageSquare size={21} />
                        <strong>{recording.title}</strong>
                        <span>باز کردن متن پیام</span>
                      </summary>
                      <div className="recording-body">
                        <p className="recording-context">{recording.context}</p>
                        <RichText text={recording.markdown} onNavigate={openFile} breaks />
                      </div>
                    </details>
                  ))}
                </div>
              )}
            </section>
          ) : tab === 'missions' ? (
            <section className="section">
              <span className="eyebrow">ساختارِ کمپینِ ۳۰–۴۰ ساعته · {editionLabel}</span>
              <h1>
                ۱۵ فصل، {fa(activeLib.budget.main_missions.length)} مأموریتِ اصلی، {fa(activeLib.sideStories.length)}{' '}
                مأموریت و معمای فرعی
              </h1>
              <p className="lead">
                {isV13
                  ? '۱۳ فصلِ اکشنِ جاده‌ای، خودرویی و نفوذِ تاکتیکی در کویرِ لوت (کاروانسرا، کمپ‌های ۱ و ۲، ورکشاپ، شبیخون‌های پیرامونی D01–D03، حریقِ D04، بازارِ سیاهِ پویا و باندِ نمکزار) + ۲ قلهٔ متمرکزِ وحشتِ بقای Mk-1 در اعماقِ تنگه (فصل ۶ و ۱۲).'
                  : isV12
                    ? 'اکشنِ تاکتیکی در کویرِ لوت (کاروانسرا، کمپ، ورکشاپ، دفاع از پایگاه، بازارِ سیاهِ پویا، باندِ پروازِ نمکزار، سنگ‌نگاره‌ها و آبشخورها) در بیرونِ تنگه و ۲ قلهٔ فشردهٔ وحشتِ بقا در اعماقِ تنگه (فصل ۶ و ۱۲).'
                    : 'اکشنِ جهان‌باز در کویرِ لوت (کاروانسرا، کمپ، ورکشاپ، دفاع از پایگاه، تورلیدرِ دردسرساز، سنگ‌نگاره‌ها و آبشخورها) در بیرونِ تنگه و ۲ فصلِ نادر و هولناکِ وحشت در اعماقِ تنگه (فصل ۶ و ۱۲).'}
              </p>
              <div className="segmented">
                {[
                  ['main', `${fa(activeLib.budget.main_missions.length)} مأموریت اصلی`],
                  ['side', `${fa(activeLib.sideStories.length)} مأموریت فرعی و دفاع از پایگاه`],
                  ['explore', 'ورکشاپ، سنگ‌نگاره‌ها و آبشخورها'],
                ].map(([id, t]) => (
                  <button key={id} className={missionMode === id ? 'selected' : ''} onClick={() => setMissionMode(id)}>
                    {t}
                  </button>
                ))}
              </div>
              {missionMode === 'main' ? (
                <>
                  <div className="chapter-selector">
                    {activeLib.chapters.map((c) => (
                      <button
                        key={c.number}
                        className={c.number === chapter ? 'selected' : ''}
                        onClick={() => setChapter(c.number)}
                      >
                        فصل {fa(c.number)}
                      </button>
                    ))}
                  </div>
                  <div className="chapter-intro">
                    <span className="eyebrow">
                      فصل {fa(chapter)} · هدف {fa(activeLib.chapters[chapter - 1]?.minutes || 0)} دقیقه
                    </span>
                    <h2>{activeLib.chapters[chapter - 1]?.title}</h2>
                    <p>{activeLib.chapterSummaries[chapter - 1]}</p>
                  </div>
                  <div className="mission-list">
                    {activeLib.budget.main_missions
                      .filter((m: any) => m.chapter === chapter)
                      .map((m: any) => (
                        <article key={m.id}>
                          <span className="mission-id" dir="ltr">
                            {m.id}
                          </span>
                          <div>
                            <h3>{m.title_fa}</h3>
                            <p>{m.focus_tags_fa?.join(' · ') || 'اکشن و پیشروی داستان'}</p>
                            <div className="mission-tags">
                              <span>{fa(m.minutes)} دقیقهٔ هدف</span>
                              <span>
                                {(
                                  {
                                    R01: 'شهداد',
                                    R02: 'نبکا و آبشخور',
                                    R03: 'کلوت‌ها',
                                    R04: 'نیروگاه خورشیدی',
                                    R05: isModern ? 'نمکزار و باندِ پرواز' : 'دشتِ نمک',
                                    R06: 'کاروانسرا / کمپ',
                                    R07: 'رصدگاه',
                                    R08: 'تنگهٔ هور',
                                  } as any
                                )[m.primary_region] || m.primary_region}
                              </span>
                            </div>
                          </div>
                          <button
                            className="text-link"
                            onClick={() => {
                              setReadOk(true);
                              setReadIdx(chapter - 1);
                              navigate('read');
                            }}
                          >
                            خواندن در فیلم‌نامه
                          </button>
                        </article>
                      ))}
                  </div>
                </>
              ) : missionMode === 'side' ? (
                <div className="side-stories">
                  {activeLib.sideStories.map((s) => (
                    <details key={s.id}>
                      <summary>
                        <span className="mission-id" dir="ltr">
                          {s.id}
                        </span>
                        <strong>{s.title}</strong>
                        <span>مأموریتِ جانبی</span>
                      </summary>
                      <RichText text={s.markdown} onNavigate={openFile} />
                    </details>
                  ))}
                </div>
              ) : (
                <div className="explore-panel">
                  <h2>سلاح، ورکشاپ و تیونینگِ آفرود، دفاع از پایگاه، سنگ‌نگاره‌ها و آبشخورها</h2>
                  <p>
                    تمامِ سیستم‌های دنیای باز، جمع‌آوریِ آیتم و کرفتینگ در ورکشاپ، تعمیر و تیونینگِ وسایل نقلیه، شبیخون
                    و بازپس‌گیریِ منابعِ پایگاه، زنجیرهٔ ۶ سنگ‌نگاره و حکاکیِ غار، ۴ آبشخور و ۱۲ عکسِ طبیعت/تحقیقی در
                    اسنادِ کاملِ زیر در دسترس‌اند.
                  </p>
                  {isV13 ? (
                    <>
                      <button className="primary" onClick={() => openDoc('05_GAMEPLAY_FA', '', 'full')}>
                        گیم‌پلی، افعال و ماتریسِ مأموریت‌ها (M00–M40)
                      </button>
                      <button className="secondary" onClick={() => openDoc('PLACES_OF_LOT_FA', '', 'full')}>
                        جهان، مکان‌ها، ناوگان و سلاح‌ها
                      </button>
                      <button className="secondary" onClick={() => openDoc('DIRECTOR_PRINCIPLES_FA', '', 'full')}>
                        منشورِ کارگردانی و برشِ عمودیِ دمو
                      </button>
                      <button className="secondary" onClick={() => openDoc('00_CANON_LEDGER_FA', '', 'full')}>
                        دفترِ کلِ کانن (نسخهٔ ۱۳)
                      </button>
                    </>
                  ) : (
                    <>
                      <button
                        className="primary"
                        onClick={() => openDoc('06_WEAPONS_CRAFTING_AND_WORKSHOP_FA', '', 'full')}
                      >
                        طراحی سلاح، ورکشاپ و تیونینگ
                      </button>
                      <button
                        className="secondary"
                        onClick={() => openDoc('07_CAMP_CARAVANSERAI_WORKSHOP_WATERHOLES_FA', '', 'full')}
                      >
                        مأموریت‌ها، پایگاه، سنگ‌نگاره‌ها و آبشخورها
                      </button>
                      <button
                        className="secondary"
                        onClick={() => openDoc('05_DIRECTION_MISE_EN_SCENE_AND_EASTER_EGGS_FA', '', 'full')}
                      >
                        سند کارگردانی، میزانسن و ۱۸ ایستر‌اگ
                      </button>
                    </>
                  )}
                </div>
              )}
            </section>
          ) : tab === 'maps' ? (
            <section className="section">
              <span className="eyebrow">واقعیت جغرافیایی و طراحی جهان</span>
              <h1>یک منطقهٔ واقعی، یک جهان داستانی</h1>
              <p className="lead">{activeLib.copy.mapLead}</p>
              <div className="segmented">
                {[
                  ['region-map', 'منطقهٔ واقعی'],
                  ['canyon-map', 'محدودهٔ تنگه'],
                  ['design-map', 'شماتیک بازی'],
                ].map(([id, t]) => (
                  <button key={id} className={map === id ? 'selected' : ''} onClick={() => setMap(id)}>
                    {t}
                  </button>
                ))}
              </div>
              <button className="map-frame" onClick={() => setLightbox(map)} aria-label="بزرگ کردن نقشه">
                <img
                  src={media(map)}
                  alt={
                    map === 'region-map'
                      ? 'نقشهٔ منطقه‌ای واقعی'
                      : map === 'canyon-map'
                        ? 'محدودهٔ تنگه'
                        : 'شماتیک اتصال مناطق بازی'
                  }
                />
                <span>برای بزرگ‌نمایی انتخاب کنید</span>
              </button>
              <p style={{ marginTop: 18 }}>
                <a className="secondary" href={mapUrl()} target="_blank" rel="noopener noreferrer">
                  باز کردن نقشهٔ تعاملی در صفحهٔ جدا
                </a>
              </p>
              <div className="map-context">
                <h2>{activeLib.copy.mapTitles[['region-map', 'canyon-map', 'design-map'].indexOf(map)]}</h2>
                <p>{activeLib.copy.mapTexts[['region-map', 'canyon-map', 'design-map'].indexOf(map)]}</p>
                <small>
                  تصاویر پایه: Esri، Vantor، Earthstar Geographics، GIS User Community · راه‌ها: © OpenStreetMap
                  contributors.
                </small>
              </div>
              <div className="two-cards">
                <button className="path-card" onClick={() => openDoc('GEOGRAPHY_EVIDENCE_FA')}>
                  <h3>منابع و دقت جغرافیایی</h3>
                  <p>مختصات، فاصله‌ها و آنچه هنوز قطعی نیست.</p>
                  <span className="text-link">خواندن شواهد</span>
                </button>
                <button
                  className="path-card"
                  onClick={() =>
                    openDoc(isV13 ? 'PLACES_OF_LOT_FA' : '04_OPEN_WORLD_SYSTEMS_AND_VISUAL_BIBLE_FA', '', 'full')
                  }
                >
                  <h3>۶ ناحیهٔ دنیای باز و تنگه ({edition})</h3>
                  <p>نقشِ هر منطقه در سواری، اکشن و داستان.</p>
                  <span className="text-link">خواندن طراحی جهان</span>
                </button>
              </div>
            </section>
          ) : tab === 'tango' ? (
            <TangoPage />
          ) : tab === 'gallery' || tab === 'vehicles' ? (
            <section className="section">
              <span className="eyebrow">آرشیوِ رسانه‌های ردِ هور</span>
              <h1>{tab === 'vehicles' ? 'وسیله‌ها و طراحیِ ناوگان' : 'گالری تصاویر، ویدیو و موسیقی'}</h1>
              <p className="lead">
                {tab === 'vehicles'
                  ? 'طرح‌های خودروها، موتور، چهارچرخ، کامیون و شتر؛ برای دیدن هر تصویر آن را انتخاب کنید.'
                  : 'تصاویر مفهومی، فیلم‌های واقعیِ منطقه، ویدیوهای پروژه و موسیقی‌های ساخته‌شده برای ردِ هور.'}
              </p>
              {tab === 'gallery' && (
                <div className="segmented media-tabs">
                  {[
                    ['images', 'تصاویر'],
                    ['videos', 'ویدیوها'],
                    ['music', 'موسیقی'],
                  ].map(([id, title]) => (
                    <button
                      key={id}
                      className={galleryMediaMode === id ? 'selected' : ''}
                      onClick={() => setGalleryMediaMode(id)}
                    >
                      {id === 'music' ? <Music2 size={17} /> : id === 'videos' ? <Play size={17} /> : <Images size={17} />}{' '}
                      {title}
                    </button>
                  ))}
                </div>
              )}
              {tab === 'vehicles' || galleryMediaMode === 'images' ? (
                <>
                  {tab === 'gallery' && (
                    <div className="filter-row">
                      {['همه', ...new Set(activeLib.gallery.map((p) => p.category))].map((c) => (
                        <button key={c} className={c === category ? 'selected' : ''} onClick={() => setCategory(c)}>
                          {c}
                        </button>
                      ))}
                    </div>
                  )}
                  <div className="gallery">
                    {activeLib.gallery
                      .filter((p) => (tab === 'vehicles' ? p.category === 'وسیله' : category === 'همه' || p.category === category))
                      .map((p) => (
                        <button className="picture-card" key={p.id} onClick={() => setLightbox(p.id)}>
                          <img src={media(p.id)} alt={p.title + ' — ' + p.filename} loading="lazy" />
                          <div>
                            <span className={'tag ' + (p.retired ? 'retired' : '')}>
                              {p.retired ? 'ایدهٔ کنارگذاشته‌شده' : p.category}
                            </span>
                            <h3>{p.title}</h3>
                            <small dir="ltr">{p.filename}</small>
                          </div>
                        </button>
                      ))}
                  </div>
                </>
              ) : galleryMediaMode === 'videos' ? (
                <div className="media-gallery">
                  {galleryVideos.map((v) => (
                    <article className="media-card" key={v.src}>
                      <video controls playsInline preload="metadata" src={v.src} />
                      <div>
                        <span className="tag">ویدیو</span>
                        <h2>{v.title}</h2>
                        <p>{v.note}</p>
                      </div>
                    </article>
                  ))}
                </div>
              ) : (
                <div className="music-gallery">
                  {musicTracks.map((track, i) => (
                    <article className="music-card" key={track.file}>
                      <div className="music-art">
                        <Music2 size={30} />
                        <span>ردِ هور · {fa(i + 1)}</span>
                      </div>
                      <div>
                        <span className="eyebrow">موسیقیِ پروژه</span>
                        <h2>{track.title}</h2>
                        <p>{track.subtitle}</p>
                        <audio controls preload="metadata" src={galleryMediaUrl(track.file)} />
                      </div>
                    </article>
                  ))}
                </div>
              )}
            </section>
          ) : (
            <section className="section">
              <span className="eyebrow">همهٔ نوشته‌ها در یک جا · {editionLabel}</span>
              <h1>داستان و راهنمای کامل بازی ({editionLabel})</h1>
              <p className="lead">
                {isV13
                  ? 'اسنادِ نسخهٔ ۱۳ (سنتزِ نهاییِ کانن) مرجعِ رسمی و قفل‌شدهٔ پروژه هستند؛ از دفترِ کلِ کانن و گاه‌شمار تا فیلم‌نامه و رمانِ کامل.'
                  : isV12
                    ? 'اسنادِ نسخهٔ ۱۲ (بازار بین‌المللی — اکشنِ خالص) آرشیوِ نسخهٔ قبل‌اند؛ متنِ کاملِ Markdown هر سند در دسترس است.'
                    : 'اسنادِ نسخهٔ ۱۱ (بازطراحی AAA) آرشیوِ درامِ بومی‌اند؛ برای هر سند هم توضیحِ ساده و هم متنِ کاملِ Markdown در دسترس است.'}
              </p>
              <div className="filter-row">
                {['همه', ...new Set(activeLib.docs.map((d) => d.category))].map((c) => (
                  <button key={c} className={c === category ? 'selected' : ''} onClick={() => setCategory(c)}>
                    {c}
                  </button>
                ))}
              </div>
              <div className="document-cards">
                {activeLib.docs
                  .filter((d) => category === 'همه' || d.category === category)
                  .map((d) => {
                    const hasPlain = !!activeLib.readerEdition?.[d.id];
                    return (
                      <article className="document-card" key={d.id}>
                        <div>
                          <span className={'tag ' + (d.legacy ? 'retired' : '')}>{d.category}</span>
                          <small>
                            {fa(
                              Math.ceil(
                                (activeLib.readerEdition?.[d.id]?.markdown || d.markdown).split(/\s+/).length / 190,
                              ),
                            )}{' '}
                            دقیقه
                          </small>
                        </div>
                        <h2>
                          <a
                            href={documentHref(d.id, hasPlain ? 'read' : 'full')}
                            onClick={(e) => {
                              e.preventDefault();
                              openDoc(d.id, '', hasPlain ? 'read' : 'full');
                            }}
                          >
                            {activeLib.readerEdition?.[d.id]?.title || d.title}
                          </a>
                        </h2>
                        <p>{d.description}</p>
                        <div className="doc-card-links">
                          {hasPlain && (
                            <a
                              className="text-link"
                              href={documentHref(d.id, 'read')}
                              onClick={(e) => {
                                e.preventDefault();
                                openDoc(d.id, '', 'read');
                              }}
                            >
                              خواندن توضیح ساده
                            </a>
                          )}
                          <a
                            className="text-link"
                            href={documentHref(d.id, 'full')}
                            onClick={(e) => {
                              e.preventDefault();
                              openDoc(d.id, '', 'full');
                            }}
                          >
                            متن کامل در Markdown
                          </a>
                        </div>
                        {d.spoiler && <small className="muted">شامل جزئیات و پایان داستان</small>}
                      </article>
                    );
                  })}
              </div>
            </section>
          )}
        </main>
        <footer className="footer">
          <span>ردِ هور · {editionTag}</span>
          <span>رمان، فیلم‌نامه و کتابِ طراحیِ بازی</span>
        </footer>
      </div>
      {lightbox && (
        <div
          className="lightbox"
          role="dialog"
          aria-modal="true"
          aria-label={pic?.title || 'نقشهٔ بزرگ'}
          onClick={() => setLightbox(null)}
        >
          <button className="lightbox-close icon-button" onClick={() => setLightbox(null)} aria-label="بستن تصویر">
            <X />
          </button>
          <div className="lightbox-inner" onClick={(e) => e.stopPropagation()}>
            <img src={media(lightbox)} alt={pic?.title || 'نقشهٔ بزرگ'} />
            <div>
              <h2>{pic?.title || 'نقشهٔ ردِ هور'}</h2>
              <p>{pic?.caption || 'نقشهٔ مطالعاتی طراحی؛ برای مسیریابی میدانی استفاده نشود.'}</p>
              {pic && <small dir="ltr">{pic.filename}</small>}
            </div>
            {pic && (
              <div className="lightbox-nav">
                <button
                  className="secondary"
                  onClick={() => {
                    const i = activeLib.gallery.indexOf(pic);
                    setLightbox(activeLib.gallery[(i + activeLib.gallery.length - 1) % activeLib.gallery.length].id);
                  }}
                >
                  <ChevronRight size={18} /> قبلی
                </button>
                <span>
                  {fa(activeLib.gallery.indexOf(pic) + 1)} از {fa(activeLib.gallery.length)}
                </span>
                <button
                  className="secondary"
                  onClick={() => {
                    const i = activeLib.gallery.indexOf(pic);
                    setLightbox(activeLib.gallery[(i + 1) % activeLib.gallery.length].id);
                  }}
                >
                  بعدی <ChevronLeft size={18} />
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
