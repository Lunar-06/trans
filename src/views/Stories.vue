<template>
  <div class="stories-page">
    <div class="container">
      <header class="page-header" v-if="!selectedStory">
        <h1 class="page-title">民俗特色</h1>
      </header>
      <br>
      <br>

      <!-- 筛选区域 -->
      <div class="filter-section" v-if="!selectedStory">
        <div class="filter-group">
          <span class="filter-label">故事类型：</span>
          <button
            v-for="type in storyTypes"
            :key="type.id"
            class="filter-btn"
            :class="{ active: selectedType === type.id }"
            @click="selectedType = type.id"
          >
            {{ type.name }}
          </button>
        </div>
        <div class="filter-group">
          <span class="filter-label">地区：</span>
          <select v-model="selectedRegion" class="region-select">
            <option value="all">全部</option>
            <option v-for="region in regions" :key="region" :value="region">
              {{ region }}
            </option>
          </select>
        </div>
      </div>

      <!-- 主内容区 -->
      <div class="main-content" v-if="!selectedStory">
        <!-- 左侧故事列表 -->
        <div class="stories-list">
          <div
            v-for="(story, index) in filteredStories"
            :key="story.id"
            class="story-card"
            @click="viewStory(story)"
          >
            <div class="story-item">
              <div class="story-image">
                <img :src="story.image" alt="故事图片">
              </div>
              <div class="story-content">
                <h3 class="story-title">{{ story.title }}</h3>
                <p class="story-excerpt">{{ story.excerpt }}</p>
              </div>
            </div>
            <div class="story-divider" v-if="index < filteredStories.length - 1"></div>
          </div>
        </div>

        <!-- 右侧热搜词条 -->
        <div class="hot-search">
          <div class="hot-search-header">
            <h3>热搜词条</h3>
          </div>
          <div class="hot-search-list">
            <div
              v-for="(item, index) in hotSearchList"
              :key="index"
              class="hot-search-item"
            >
              <span class="hot-rank" :class="{ 'hot': index < 3 }">
                {{ index + 1 }}
              </span>
              <span class="hot-title">{{ item }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 故事详情 -->
      <transition name="fade">
        <div class="story-detail" v-if="selectedStory">
          <div class="breadcrumb">
            您的位置: <a href="/">首页</a> &gt; <a href="/stories">民俗特色</a> &gt;
          </div>

          <article class="story-article">
            <header class="article-header">
              <h1 class="article-title">{{ selectedStory.title }}</h1>
            </header>

            <div class="article-body">
              <p class="lead-paragraph">{{ selectedStory.content.lead }}</p>

              <div class="story-image-container">
                <img :src="selectedStory.image" alt="故事图片" class="story-image">
              </div>

              <section
                v-for="(section, index) in selectedStory.content.sections"
                :key="index"
                class="content-section"
              >
                <p>{{ section.text }}</p>
              </section>

              <section class="content-section">
                <p>{{ selectedStory.content.conclusion.text }}</p>
              </section>
            </div>
          </article>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// 筛选条件
const selectedType = ref('all')
const selectedRegion = ref('all')
const selectedStory = ref(null)

// 热搜词条
const hotSearchList = ref([
  '黄石港饼制作工艺',
  '阳新布贴艺术',
  '黄石春节习俗',
  '大冶铁矿历史',
  '黄石龙舟竞渡',
  '阳新采茶戏',
  '黄石民俗文化',
  '黄石特色美食',
  '黄石旅游景点',
  '黄石历史故事'
])

// 刷新热搜词条
const refreshHotSearch = () => {
  // 简单的刷新逻辑，实际项目中可以从后端获取
  const temp = [...hotSearchList.value]
  for (let i = temp.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[temp[i], temp[j]] = [temp[j], temp[i]]
  }
  hotSearchList.value = temp
}

// 故事分类（固定不变，可保留前端）
const storyTypes = [
  { id: 'all', name: '全部' },
  { id: 'legend', name: '民间传说' },
  { id: 'custom', name: '民俗习惯' },
  { id: 'festival', name: '节日故事' },
  { id: 'craft', name: '手艺传承' }
]

// 故事列表（前端静态数据）
const stories = ref([
  {
    id: 1,
    title: '黄石港饼的传说',
    subtitle: '一段关于黄石特色美食的传奇故事',
    image: new URL('../assets/港饼.jpg', import.meta.url).href,
    type: 'legend',
    typeName: '民间传说',
    region: '湖北黄石',
    excerpt: '黄石港饼是黄石的传统名点，有着悠久的历史和丰富的文化内涵。相传在清朝时期，一位糕点师傅在黄石港码头附近开店，为了吸引顾客，他创制了一种独特的饼...',
    content: {
      lead: '黄石港饼是黄石的传统名点，有着悠久的历史和丰富的文化内涵。相传在清朝时期，一位糕点师傅在黄石港码头附近开店，为了吸引顾客，他创制了一种独特的饼。',
      sections: [
        {
          heading: '起源与传说',
          text: '据说，黄石港饼的起源与一位名叫王福的糕点师傅有关。他在黄石港码头附近经营着一家小糕点店，为了吸引过往的商人和旅客，他不断改进自己的糕点制作技艺。有一天，他突发奇想，将面粉、芝麻、冰糖等原料混合在一起，制作出一种口感酥脆、甜而不腻的饼。这种饼一经推出，就受到了顾客的喜爱，逐渐成为黄石的特色美食。'
        },
        {
          heading: '制作工艺',
          text: '黄石港饼的制作工艺十分讲究，需要经过选料、配料、揉面、成型、烘烤等多个环节。选用优质面粉、芝麻、冰糖、桂花等原料，经过精心调配，制作出的港饼外观金黄，口感酥脆，甜而不腻，带有浓郁的芝麻香味。'
        },
        {
          heading: '文化内涵',
          text: '黄石港饼不仅是一种美食，更是黄石文化的重要组成部分。它见证了黄石的历史变迁，承载着黄石人民的情感记忆。如今，黄石港饼已经成为黄石的一张文化名片，深受当地居民和游客的喜爱。'
        }
      ],
      quote: '黄石港饼，甜在口中，香在心里，是黄石人民的骄傲。',
      conclusion: {
        heading: '传承与发展',
        text: '随着时代的发展，黄石港饼的制作工艺不断创新，但始终保持着传统的风味。如今，黄石港饼已经走出黄石，走向全国，成为中国传统糕点的代表之一。它不仅是一种美食，更是黄石文化的传承和发扬。'
      }
    }
  },
  {
    id: 2,
    title: '阳新布贴的艺术',
    subtitle: '传承千年的民间手工艺',
    image: new URL('../assets/布贴.jpg', import.meta.url).href,
    type: 'craft',
    typeName: '手艺传承',
    region: '湖北黄石阳新',
    excerpt: '阳新布贴是阳新县的传统民间手工艺，有着悠久的历史。它以色彩鲜艳、图案精美、工艺精湛而闻名，是中国民间艺术的瑰宝...',
    content: {
      lead: '阳新布贴是阳新县的传统民间手工艺，有着悠久的历史。它以色彩鲜艳、图案精美、工艺精湛而闻名，是中国民间艺术的瑰宝。',
      sections: [
        {
          heading: '历史渊源',
          text: '阳新布贴的历史可以追溯到明清时期，当时阳新的妇女们为了装饰自己的衣物和家居用品，开始用各种颜色的布料制作布贴。经过几百年的发展，阳新布贴逐渐形成了自己独特的艺术风格。'
        },
        {
          heading: '制作工艺',
          text: '阳新布贴的制作工艺十分复杂，需要经过设计、裁剪、粘贴、缝制等多个环节。艺人们根据不同的主题和用途，设计出各种精美的图案，然后用剪刀将布料剪成所需的形状，再用糨糊粘贴在底布上，最后用针线缝制固定。'
        },
        {
          heading: '艺术特色',
          text: '阳新布贴的艺术特色主要体现在色彩、图案和构图上。它使用鲜艳的色彩，搭配和谐，给人以视觉上的享受。图案题材广泛，包括花鸟、人物、山水等，富有浓郁的民间特色。构图饱满，布局合理，给人以平衡感和美感。'
        }
      ],
      quote: '阳新布贴，一针一线都是艺术，一布一贴都是文化。',
      conclusion: {
        heading: '传承与保护',
        text: '如今，阳新布贴已经被列入国家级非物质文化遗产名录，得到了政府和社会的重视。许多年轻人开始学习阳新布贴的制作工艺，为这一传统艺术的传承和发展注入了新的活力。阳新布贴不仅是阳新人民的骄傲，更是中国民间艺术的宝贵财富。'
      }
    }
  },
  {
    id: 3,
    title: '黄石的春节习俗',
    subtitle: '传统节日的独特魅力',
    image: new URL('../assets/春节习俗.jpg', import.meta.url).href,
    type: 'festival',
    typeName: '节日故事',
    region: '湖北黄石',
    excerpt: '春节是中国最重要的传统节日，黄石地区的春节习俗有着自己独特的特色。从腊月二十三的小年开始，到正月十五的元宵节结束，黄石人民用各种方式庆祝这个喜庆的节日...',
    content: {
      lead: '春节是中国最重要的传统节日，黄石地区的春节习俗有着自己独特的特色。从腊月二十三的小年开始，到正月十五的元宵节结束，黄石人民用各种方式庆祝这个喜庆的节日。',
      sections: [
        {
          heading: '小年祭灶',
          text: '腊月二十三是小年，黄石地区有祭灶的习俗。人们会在灶台上摆放糖果、糕点等供品，祭祀灶王爷，希望他在向玉皇大帝汇报时多说好话，保佑全家平安幸福。'
        },
        {
          heading: '除夕守岁',
          text: '除夕之夜，黄石人民会全家团聚，吃年夜饭，守岁到深夜。年夜饭通常包括鱼、肉、饺子等象征吉祥的食物，寓意着年年有余、团圆美满。守岁时，人们会放鞭炮、贴春联、挂灯笼，营造出喜庆的节日氛围。'
        },
        {
          heading: '正月初一拜年',
          text: '正月初一，黄石人民会穿上新衣服，走亲访友，互相拜年。拜年时，人们会说一些吉祥如意的话，给孩子们发压岁钱，表达对新年的美好祝愿。'
        },
        {
          heading: '元宵节闹花灯',
          text: '正月十五是元宵节，黄石地区有闹花灯的习俗。人们会制作各种精美的花灯，举行花灯展和灯谜活动，晚上还会放烟花，热闹非凡。'
        }
      ],
      quote: '春节是团圆的节日，是希望的节日，是黄石人民最喜庆的节日。',
      conclusion: {
        heading: '传统与现代',
        text: '随着时代的发展，黄石地区的春节习俗也在不断变化，但传统的核心内容始终保持不变。人们依然会团聚、拜年、放鞭炮，依然会用各种方式表达对新年的美好祝愿。春节不仅是一个传统节日，更是黄石人民情感的纽带，是黄石文化的重要组成部分。'
      }
    }
  },
  {
    id: 4,
    title: '大冶铁矿的故事',
    subtitle: '一座矿山的历史与传奇',
    image: new URL('../assets/铁矿.jpg', import.meta.url).href,
    type: 'legend',
    typeName: '民间传说',
    region: '湖北黄石大冶',
    excerpt: '大冶铁矿是中国著名的铁矿之一，有着悠久的历史。关于大冶铁矿的起源，当地流传着许多美丽的传说...',
    content: {
      lead: '大冶铁矿是中国著名的铁矿之一，有着悠久的历史。关于大冶铁矿的起源，当地流传着许多美丽的传说。',
      sections: [
        {
          heading: '铁矿的发现',
          text: '相传在古代，有一位名叫李铁的铁匠，他在大冶的一座山上发现了铁矿石。他用这些铁矿石打造出了锋利的武器和工具，受到了当地人民的尊敬。后来，人们就把这座山称为铁山，把这里的铁矿称为大冶铁矿。'
        },
        {
          heading: '矿山的发展',
          text: '大冶铁矿的开采历史可以追溯到春秋战国时期，当时人们就开始在这里开采铁矿石。经过几千年的发展，大冶铁矿逐渐成为中国重要的铁矿基地。特别是在近代，大冶铁矿为中国的工业发展做出了重要贡献。'
        },
        {
          heading: '矿山的文化',
          text: '大冶铁矿不仅是一座矿山，更是一座文化宝库。它见证了中国矿业的发展历史，承载着矿工们的辛勤付出和智慧结晶。如今，大冶铁矿已经成为黄石的一个重要旅游景点，吸引着众多游客前来参观。'
        }
      ],
      quote: '大冶铁矿，是黄石的骄傲，是中国矿业的瑰宝。',
      conclusion: {
        heading: '未来与希望',
        text: '随着时代的发展，大冶铁矿的开采技术不断创新，矿山的环境也得到了改善。如今，大冶铁矿已经从单一的矿业生产转型为集矿业、旅游、文化于一体的综合性产业基地。它不仅为黄石的经济发展做出了贡献，也为中国的矿业发展树立了榜样。'
      }
    }
  },
  {
    id: 5,
    title: '黄石的龙舟竞渡',
    subtitle: '端午节的传统活动',
    image: new URL('../assets/龙舟竞渡.jpg', import.meta.url).href,
    type: 'custom',
    typeName: '民俗习惯',
    region: '湖北黄石',
    excerpt: '龙舟竞渡是黄石地区端午节的传统活动，有着悠久的历史。每年端午节，黄石的江河湖泊上都会举行盛大的龙舟比赛...',
    content: {
      lead: '龙舟竞渡是黄石地区端午节的传统活动，有着悠久的历史。每年端午节，黄石的江河湖泊上都会举行盛大的龙舟比赛。',
      sections: [
        {
          heading: '起源与传说',
          text: '龙舟竞渡的起源与屈原有关。相传，屈原投江后，当地人民为了防止鱼虾啃食他的身体，就用竹筒装米投入江中，后来逐渐演变成了端午节吃粽子的习俗。同时，人们还划着船在江中寻找屈原的尸体，这就是龙舟竞渡的起源。'
        },
        {
          heading: '比赛形式',
          text: '黄石地区的龙舟比赛通常在端午节当天举行。参赛的龙舟队由几十人组成，他们穿着统一的服装，手持船桨，在锣鼓声中奋力划桨，向着终点冲刺。比赛现场人山人海，热闹非凡。'
        },
        {
          heading: '文化意义',
          text: '龙舟竞渡不仅是一项体育活动，更是一种文化传承。它体现了黄石人民团结协作、奋勇拼搏的精神，也表达了人们对屈原的敬仰和怀念之情。如今，龙舟竞渡已经成为黄石地区端午节的重要组成部分，吸引着越来越多的人参与其中。'
        }
      ],
      quote: '龙舟竞渡，是力量的较量，是团结的象征，是黄石人民的精神写照。',
      conclusion: {
        heading: '传承与发展',
        text: '随着时代的发展，黄石地区的龙舟竞渡活动不断创新，不仅保留了传统的比赛形式，还增加了许多新的元素。如今，龙舟竞渡已经成为黄石的一张文化名片，吸引着众多游客前来观看。它不仅是黄石人民的骄傲，更是中国传统民俗的重要组成部分。'
      }
    }
  },
  {
    id: 6,
    title: '阳新采茶戏',
    subtitle: '民间戏曲的瑰宝',
    image: new URL('../assets/阳新采茶戏.jpg', import.meta.url).href,
    type: 'craft',
    typeName: '手艺传承',
    region: '湖北黄石阳新',
    excerpt: '阳新采茶戏是阳新县的传统戏曲剧种，有着悠久的历史。它以优美的唱腔、生动的表演、丰富的剧目而闻名...',
    content: {
      lead: '阳新采茶戏是阳新县的传统戏曲剧种，有着悠久的历史。它以优美的唱腔、生动的表演、丰富的剧目而闻名。',
      sections: [
        {
          heading: '历史渊源',
          text: '阳新采茶戏起源于明清时期，当时阳新的茶农在采茶时，为了缓解疲劳，就会唱一些山歌和小调。后来，这些山歌和小调逐渐发展成为一种戏曲形式，就是阳新采茶戏。'
        },
        {
          heading: '艺术特色',
          text: '阳新采茶戏的艺术特色主要体现在唱腔、表演和剧目上。它的唱腔优美动听，富有地方特色；表演生动形象，注重情感表达；剧目内容丰富，包括爱情故事、历史传说、民间生活等多个方面。'
        },
        {
          heading: '传承与发展',
          text: '阳新采茶戏是阳新人民的文化瑰宝，也是中国民间戏曲的重要组成部分。如今，阳新采茶戏已经被列入国家级非物质文化遗产名录，得到了政府和社会的重视。许多年轻人开始学习阳新采茶戏的表演技艺，为这一传统艺术的传承和发展注入了新的活力。'
        }
      ],
      quote: '阳新采茶戏，是阳新人民的精神食粮，是中国民间戏曲的瑰宝。',
      conclusion: {
        heading: '未来与希望',
        text: '随着时代的发展，阳新采茶戏的表演形式和内容不断创新，但始终保持着传统的艺术特色。如今，阳新采茶戏已经走出阳新，走向全国，成为中国民间戏曲的代表之一。它不仅是阳新人民的骄傲，更是中国文化的重要组成部分。'
      }
    }
  }
])

// 筛选逻辑（不变）
const filteredStories = computed(() => {
  let result = stories.value

  if (selectedType.value !== 'all') {
    result = result.filter(s => s.type === selectedType.value)
  }

  if (selectedRegion.value !== 'all') {
    result = result.filter(s => s.region === selectedRegion.value)
  }

  return result
})

// 查看故事
const viewStory = (story) => {
  selectedStory.value = story
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<style scoped>
.loading {
  text-align: center;
  padding: 40px;
  font-size: 16px;
  color: #666;
}

.stories-page {
  padding: 40px 0 80px;
}

.page-header {
  text-align: center;
  margin-bottom: 48px;
}

.page-title {
  font-family: var(--font-serif);
  font-size: 40px;
  font-weight: 700;
  color: var(--color-auxiliary);
  margin-bottom: 16px;
}

.page-desc {
  font-size: 18px;
  color: var(--color-text-light);
}

.filter-section {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  margin-bottom: 40px;
  padding: 24px;
  background: var(--color-white);
  box-shadow: var(--shadow-sm);
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-label {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text);
}

.filter-btn {
  padding: 8px 16px;
  background: var(--color-background);
  border-radius: var(--radius-sm);
  font-size: 14px;
  transition: all var(--transition-fast);
}

.filter-btn:hover {
  background: rgba(139, 69, 19, 0.1);
}

.filter-btn.active {
  background: var(--color-primary);
  color: var(--color-white);
}

.region-select {
  padding: 8px 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-size: 14px;
  background: var(--color-white);
  cursor: pointer;
}

.main-content {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 32px;
}

.stories-list {
  display: flex;
  flex-direction: column;
}

.story-card {
  background: var(--color-white);
  overflow: hidden;
  cursor: pointer;
  transition: all var(--transition-normal);
  padding: 24px;
}

.story-card:hover {
  background: #f5f5f5;
}

.story-item {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.story-image {
  width: 150px;
  height: 100px;
  flex-shrink: 0;
  overflow: hidden;
  border-radius: 4px;
}

.story-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.story-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.story-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text);
  margin: 0;
  line-height: 1.4;
}

.story-excerpt {
  font-size: 14px;
  color: var(--color-text-light);
  line-height: 1.6;
  margin: 0;
  display: -webkit-box;
  display: box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  box-orient: vertical;
  overflow: hidden;
}

.story-divider {
  height: 1px;
  background-color: var(--color-border);
  margin: 20px 0;
}

.card-icon {
  font-size: 24px;
}

/* 热搜词条样式 */
.hot-search {
  background: var(--color-white);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  padding: 24px;
  height: fit-content;
  position: sticky;
  top: 24px;
}

.hot-search-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.hot-search-header h3 {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-auxiliary);
}

.hot-search-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.hot-search-item {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.hot-search-item:hover {
  color: var(--color-primary);
}

.hot-rank {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  background: var(--color-background);
  color: var(--color-text-light);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
}

.hot-rank.hot {
  background: #ff4757;
  color: var(--color-white);
}

.hot-title {
  font-size: 14px;
  line-height: 1.5;
  flex: 1;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid var(--color-border);
  margin-top: 8px;
}

.card-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.tag {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.tag-type {
  background: rgba(139, 69, 19, 0.1);
  color: var(--color-primary);
}

.tag-region {
  background: var(--color-secondary);
  color: var(--color-text);
}

.card-title {
  font-family: var(--font-serif);
  font-size: 20px;
  font-weight: 700;
  color: var(--color-auxiliary);
  margin-bottom: 12px;
  line-height: 1.4;
}

.card-excerpt {
  font-size: 14px;
  color: var(--color-text-light);
  line-height: 1.7;
  margin-bottom: 16px;
  display: -webkit-box;
  display: box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  box-orient: vertical;
  overflow: hidden;
}



.story-detail {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 24px;
}

.breadcrumb {
  font-size: 14px;
  margin-bottom: 24px;
  padding-top: 24px;
}

.breadcrumb a {
  text-decoration: none;
}

.breadcrumb a:hover {
  text-decoration: underline;
}

.btn-back {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-size: 14px;
  color: var(--color-text);
  margin-bottom: 32px;
  transition: all var(--transition-fast);
}

.btn-back:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.story-article {
  background: var(--color-white);
  overflow: hidden;
  box-shadow: var(--shadow-md);
}

.article-header {
  padding: 24px 48px;
  background: var(--color-white);
  color: var(--color-text);
  margin-bottom: 32px;
}

.article-title {
  font-family: var(--font-serif);
  font-size: 32px;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 16px;
  text-align: center;
}

.article-meta-info {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  font-size: 14px;
  color: var(--color-text-light);
  margin-bottom: 24px;
  border-bottom: 1px solid var(--color-border);
  padding-bottom: 16px;
}

.article-body {
  padding: 0 48px 48px;
}

.lead-paragraph {
  font-size: 16px;
  line-height: 1.8;
  color: var(--color-text);
  margin-bottom: 32px;
  padding-bottom: 0;
  border-bottom: none;
}

.story-image-container {
  margin: 32px 0;
  text-align: left;
}

.story-image {
  width: 150px;
  height: 100px;
  object-fit: cover;
  border-radius: 4px;
}

.story-detail .story-image {
  width: 100%;
  max-width: 800px;
  height: auto;
  border-radius: 4px;
  box-shadow: none;
  display: block;
}

.content-section {
  margin-bottom: 24px;
}

.content-section p {
  font-size: 16px;
  line-height: 1.8;
  color: var(--color-text);
  margin-bottom: 16px;
  text-align: justify;
  text-indent: 2em;
}

.story-quote {
  display: none;
}

.article-footer {
  display: none;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--transition-slow);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .main-content {
    grid-template-columns: 1fr;
  }

  .hot-search {
    position: static;
  }
}

@media (max-width: 768px) {
  .filter-section {
    flex-direction: column;
    gap: 16px;
  }

  .main-content {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .story-card {
    padding: 20px;
  }

  .hot-search {
    padding: 20px;
  }

  .article-header {
    flex-direction: column;
    text-align: center;
    padding: 32px;
  }

  .article-icon {
    font-size: 64px;
  }

  .article-title {
    font-size: 28px;
  }

  .article-body {
    padding: 32px;
  }

  .article-footer {
    grid-template-columns: 1fr;
    padding: 24px 32px;
  }
}
</style>