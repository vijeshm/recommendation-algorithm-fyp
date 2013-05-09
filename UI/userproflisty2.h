#ifndef USERPROFLISTY2_H
#define USERPROFLISTY2_H

#include <QWidget>
#include <QFile>
#include <QTextStream>
#include <QProcess>
namespace Ui {
class userproflisty2;
}

class userproflisty2 : public QWidget
{
    Q_OBJECT
    
public:
    QProcess *showproc;
    QProcess *attri;
    explicit userproflisty2(QWidget *parent = 0);
    ~userproflisty2();

public slots:
    void showcompleted();
    void atrichange();
    void attribchange();
    void nectclicked();
signals:
    void movenext();
    
private:
    Ui::userproflisty2 *ui;
};

#endif // USERPROFLISTY2_H
