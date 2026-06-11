import { useState, useRef, useEffect } from 'react'

interface Msg {
  role: 'user' | 'assistant'
  content: string
  intent?: string
}

const LABELS: Record<string, string> = {
  PRESALE: '售前',
  AFTERSALE: '售后',
  MARKETING: '营销',
  GENERAL: '通用'
}

export default function App() {
  const [messages, setMessages] = useState<Msg[]>([
    { role: 'assistant', content: '你好！我是 AI 导购助手\n可以帮你查商品、查订单、写营销文案\n有什么可以帮你的？' }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  const send = async () => {
    const text = input.trim()
    if (!text || loading) return

    setMessages(prev => [...prev, { role: 'user', content: text }])
    setInput('')
    setLoading(true)

    try {
      const res = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, chat_history: [] })
      })
      const data = await res.json()
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.reply,
        intent: data.intent
      }])
    } catch {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: '抱歉，服务暂时不可用，请稍后重试。'
      }])
    }
    setLoading(false)
  }

  return (
    <div style={{
      maxWidth: 750, margin: '0 auto', height: '100vh',
      display: 'flex', flexDirection: 'column', fontFamily: 'system-ui, sans-serif'
    }}>
      {/* 顶栏 */}
      <div style={{
        background: 'linear-gradient(135deg, #667eea, #764ba2)',
        color: '#fff', padding: '18px 24px', fontSize: 18, fontWeight: 600
      }}>
        🛍️ 跨境电商 AI 导购助手
      </div>

      {/* 消息区 */}
      <div style={{ flex: 1, overflow: 'auto', padding: 20, background: '#fafbfc' }}>
        {messages.map((m, i) => (
          <div key={i} style={{ marginBottom: 14, textAlign: m.role === 'user' ? 'right' : 'left' }}>
            {m.intent && (
              <span style={{
                fontSize: 11, color: '#64748b', background: '#f1f5f9',
                padding: '2px 10px', borderRadius: 10, display: 'inline-block', marginBottom: 4
              }}>
                {LABELS[m.intent] || m.intent}
              </span>
            )}
            <div style={{
              display: 'inline-block', maxWidth: '75%', padding: '10px 16px', borderRadius: 14,
              background: m.role === 'user' ? '#667eea' : '#f1f5f9',
              color: m.role === 'user' ? '#fff' : '#1e293b',
              whiteSpace: 'pre-wrap', textAlign: 'left'
            }}>
              {m.content}
            </div>
          </div>
        ))}
        {loading && <div style={{ color: '#94a3b8', padding: 8 }}>思考中...</div>}
        <div ref={bottomRef} />
      </div>

      {/* 输入区 */}
      <div style={{
        display: 'flex', gap: 10, padding: 16, borderTop: '1px solid #e2e8f0', background: '#fff'
      }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && send()}
          placeholder="输入消息，比如：帮我查一下订单 ORD-20240501-001"
          style={{
            flex: 1, padding: '12px 16px', border: '2px solid #e2e8f0',
            borderRadius: 12, fontSize: 15, outline: 'none'
          }}
        />
        <button
          onClick={send}
          disabled={loading}
          style={{
            padding: '12px 24px', border: 'none', borderRadius: 12,
            background: loading ? '#94a3b8' : '#667eea',
            color: '#fff', fontSize: 15, fontWeight: 600, cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          发送
        </button>
      </div>
    </div>
  )
}